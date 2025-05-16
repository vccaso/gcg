# chat.py (Streamlit page)
import streamlit as st
import os
import time
from orchestrator_core import run_workflow
from memory_manager import load_memory, save_memory, list_sessions
from models.model_registry import MODEL_CATALOG, MODEL_REGISTRY
from agents.agent_registry import AGENT_CATALOG, AGENT_REGISTRY
from agents.orchestratoragent import OrchestratorAgent
from prompt_loader import PromptLoader
from agents.orchestrator.planner_agent import OrchestratorPlannerAgent
from agents.orchestrator.builder_agent import OrchestratorBuilderAgent
from agents.orchestrator.validator_agent import OrchestratorValidatorAgent
from agents.orchestrator.feedback_agent import OrchestratorFeedbackAgent

def render_chatv2_page():
    st.title("🧠 Orchestrator V2 – Iterative Flow")

    # Session management
    existing_sessions = list_sessions()
    session_id = st.sidebar.text_input("Session ID", value="v2_session")
    if session_id not in st.session_state:
        st.session_state.session_id = session_id
        st.session_state.memory = load_memory(session_id)

    # Model and Template selection
    col1, col2 = st.columns(2)

    with col1:
        model_choice = st.selectbox("🤖 Select Model", list(MODEL_REGISTRY.keys()), index=0)

    with col2:
        template_choice = st.selectbox("📄 Prompt Template", ["default"])

    # Iteration settings
    st.sidebar.header("🔁 Iteration Settings")
    target_score = st.sidebar.slider("🎯 Target Score", 0.0, 10.0, 8.5, step=0.1)
    desired_iterations = st.sidebar.number_input("✅ Desired Iterations", min_value=1, max_value=10, value=3)
    max_iterations = st.sidebar.number_input("🚨 Max Iterations", min_value=1, max_value=20, value=5)

    request_text = st.text_area("📝 Enter your orchestration request:",
                                value="Create a workflow to transcribe audio and generate subtitles",
                                height=150)

    if st.button("🚀 Run Full Iterative Flow"):
        agent_list = "\n".join([f"- {k}: {getattr(v, 'short_description', '')}" for k, v in AGENT_CATALOG.items()])
        model_list = "\n".join([f"- {k}: {getattr(v, 'short_description', '')}" for k, v in MODEL_CATALOG.items()])

        llm = MODEL_REGISTRY[model_choice](temperature=0.3)
        iteration = 0
        score = 0
        current_prompt = request_text
        plan_yaml = ""
        workflow_yaml = ""
        feedback_text = ""

        total_start_time = time.time()

        while iteration < max_iterations:
            iteration += 1
            st.info(f"🔁 Iteration {iteration}")
            st.markdown(f"**📝 Prompt Used:** {current_prompt}")

            iter_start = time.time()

            # Planner
            planner_prompt = PromptLoader().load_prompt("orchestratorplanneragent", template_choice)
            planner = OrchestratorPlannerAgent(llm, planner_prompt)
            plan_result = planner.run(request=current_prompt, agents_description=agent_list, models_description=model_list)
            plan_yaml = plan_result.get("yaml_plan", "")
            st.code(plan_yaml, language="yaml")

            # Builder
            builder_prompt = PromptLoader().load_prompt("orchestratorbuilderagent", template_choice)
            builder = OrchestratorBuilderAgent(llm, builder_prompt)
            build_result = builder.run(plan=plan_yaml)
            workflow_yaml = build_result.get("workflow", "")
            st.code(workflow_yaml, language="yaml")

            # Validator
            validator_prompt = PromptLoader().load_prompt("orchestratorvalidatoragent", template_choice)
            validator = OrchestratorValidatorAgent(llm, validator_prompt)
            validation = validator.run(workflow=workflow_yaml)
            score = validation["score"]
            st.markdown(f"**Score:** {score} | **Status:** {validation['status']}")
            st.markdown(f"**Feedback:** {validation['feedback']}")

            iter_duration = time.time() - iter_start
            st.markdown(f"**⏱️ Iteration Duration:** {iter_duration:.2f} seconds")

            if iteration >= desired_iterations and score >= target_score:
                break

            # Feedback
            feedback_prompt = PromptLoader().load_prompt("orchestratorfeedbackagent", template_choice)
            feedback_agent = OrchestratorFeedbackAgent(llm, feedback_prompt)
            feedback_result = feedback_agent.run(original_prompt=current_prompt, validation_feedback=validation["feedback"])
            current_prompt = feedback_result["new_prompt"]

        total_duration = time.time() - total_start_time
        st.success(f"🏁 Total Duration: {total_duration:.2f} seconds")

        st.session_state.memory["latest_plan"] = plan_yaml
        st.session_state.memory["latest_workflow"] = workflow_yaml
        st.session_state.memory["latest_validation"] = validation
        st.session_state.memory["history"].append({
            "request": request_text,
            "plan": plan_yaml,
            "workflow": workflow_yaml,
            "score": score,
            "feedback": validation["feedback"]
        })
        save_memory(st.session_state.memory, session_id)

    # History
    st.markdown("### 🧠 Planner History")
    for i, entry in enumerate(st.session_state.memory.get("history", []), 1):
        st.markdown(f"**{i}.** {entry['request']}")

    if st.session_state.memory.get("latest_workflow"):
        st.markdown("### 📜 Latest Workflow YAML")
        workflow_content = st.session_state.memory["latest_workflow"]
        st.code(workflow_content, language="yaml")

        filename = st.text_input("📝 Filename for Download", value="workflow_generated.yaml")
        st.download_button(
            label="💾 Download Workflow YAML",
            data=workflow_content,
            file_name=filename,
            mime="text/yaml"
        )

def render_chat_page():

    st.title("🧠 Chat")

    # Session management
    existing_sessions = list_sessions()
    session_id = st.sidebar.text_input("Session ID", value="dev_session")
    if session_id not in st.session_state:
        st.session_state.session_id = session_id
        st.session_state.memory = load_memory(session_id)

    # Model and Template selection
    col1, col2 = st.columns(2)

    with col1:
        model_choice = st.selectbox("🤖 Select Model", ["ModelGpt35Turbo", "ModelGpt4Turbo", "ModelDeepSeekCoder67", "ModelOllama"])

    with col2:
        template_choice = st.selectbox("📄 Select Prompt Template", ["default", "info"])

    # Input
    st.text_input("Ask something to the Orchestrator...", key="user_request")
    if st.button("💬 Submit"):
        if st.session_state.user_request:
            # Load the selected LLM
            llm = MODEL_REGISTRY[model_choice](temperature=0.3)

            # Load the selected prompt template
            prompt_loader = PromptLoader()
            prompt_template = prompt_loader.load_prompt("OrchestratorAgent", template_choice)

            agent = OrchestratorAgent(llm, prompt_template)
            result = agent.run(request=st.session_state.user_request, memory=st.session_state.memory)

            st.session_state.memory["history"].append({
                "request": st.session_state.user_request,
                "workflow": result.get("yaml", ""),
                "file": result.get("path")
            })
            st.session_state.memory["latest_workflow"] = result.get("path")

            save_memory(st.session_state.memory, session_id)
            st.success("Prompt processed and memory updated.")

    # History
    st.markdown("### 🧠 Conversation History")
    for i, entry in enumerate(st.session_state.memory.get("history", []), 1):
        st.markdown(f"**{i}.** {entry['request']}")

    # YAML preview
    if st.session_state.memory.get("latest_workflow"):
        st.markdown("### 📝 Latest Workflow YAML")
        with open(st.session_state.memory["latest_workflow"], encoding="utf-8") as f:
            st.code(f.read(), language="yaml")

    # Run workflow
    if st.button("🚀 Run Latest Workflow"):
        with st.spinner("Running workflow..."):
            result = run_workflow(st.session_state.memory["latest_workflow"], streamlit_mode=True)
            for step, output in result.items():
                if step == "_execution_duration":
                    continue
                st.subheader(f"Step: {step}")
                st.text(output)
            if "_execution_duration" in result:
                st.success(f"✅ Completed in {result['_execution_duration']}s")
