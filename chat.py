# chat.py (Streamlit page)
import streamlit as st
import os
from orchestrator_core import run_workflow
from memory_manager import load_memory, save_memory, list_sessions
from models.model_registry import MODEL_CATALOG, MODEL_REGISTRY
from agents.agent_registry import AGENT_CATALOG, AGENT_REGISTRY
from agents.orchestratoragent import OrchestratorAgent
from prompt_loader import PromptLoader
from agents.orchestrator.planner_agent import OrchestratorPlannerAgent
from agents.orchestrator.builder_agent import OrchestratorBuilderAgent

def render_chatv2_page():
    st.title("🧠 Orchestrator V2 – Planner Test")

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

    request_text = st.text_area("📝 Enter your orchestration request:",
                                value="Create a workflow to transcribe audio and generate subtitles",
                                height=150)

    if st.button("🧠 Run Planner Agent"):
        st.info("Running OrchestratorPlannerAgent...")

        agent_list = "\n".join([f"- {k}: {getattr(v, 'short_description', '')}" for k, v in AGENT_CATALOG.items()])
        model_list = "\n".join([f"- {k}: {getattr(v, 'short_description', '')}" for k, v in MODEL_CATALOG.items()])

        llm = MODEL_REGISTRY[model_choice](temperature=0.3)
        prompt_template = PromptLoader().load_prompt("orchestratorplanneragent", template_choice)

        planner = OrchestratorPlannerAgent(llm, prompt_template)
        result = planner.run(request=request_text,
                            agents_description=agent_list,
                            models_description=model_list)

        st.session_state.memory["history"].append({
            "request": request_text,
            "plan": result.get("yaml_plan", "")
        })
        save_memory(st.session_state.memory, session_id)
        st.success("Planner result saved to memory.")

    # History
    st.markdown("### 🧠 Planner History")
    for i, entry in enumerate(st.session_state.memory.get("history", []), 1):
        st.markdown(f"**{i}.** {entry['request']}")

    # YAML preview
    if st.session_state.memory.get("history"):
        st.markdown("### 📝 Latest YAML Plan")
        latest_plan = st.session_state.memory["history"][-1].get("plan", "")
        st.code(latest_plan, language="yaml")

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
