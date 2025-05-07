# orchestrator_chat.py (Streamlit page)
import streamlit as st
import os
from orchestrator_core import run_workflow
from memory_manager import load_memory, save_memory, list_sessions
from models.model_registry import MODEL_REGISTRY
from agents.orchestratoragent import OrchestratorAgent
from models.openai.model_gpt_35_turbo import ModelGpt35Turbo  # Default model

def render_chat_page():

    st.title("🧠 Chat")

    # Session management
    existing_sessions = list_sessions()
    session_id = st.sidebar.text_input("Session ID", value="dev_session")
    if session_id not in st.session_state:
        st.session_state.session_id = session_id
        st.session_state.memory = load_memory(session_id)

    # Input
    st.text_input("Ask something to the Orchestrator...", key="user_request")
    if st.button("💬 Submit"):
        if st.session_state.user_request:
            llm = ModelGpt35Turbo(temperature=0.3)
            agent = OrchestratorAgent(llm)
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
