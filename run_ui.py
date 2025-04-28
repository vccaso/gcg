import streamlit as st
import os
import yaml
from orchestrator_core import run_workflow
from models.model_registry import MODEL_CATALOG
from agents.agent_registry import AGENT_CATALOG
from config import __version__, __app_name__, __workflow_path__

st.set_page_config(page_title=__app_name__, page_icon="🧠")

# Sidebar menu
menu = st.sidebar.selectbox(
    "📂 Menu",
    ("Home", "Workflows", "Agents", "Models", "Config", "Templates", "Docs")
)

st.sidebar.markdown(f"<div style='text-align:center; color: gray;'>v{__version__}</div>", unsafe_allow_html=True)

# ---------------------
# 🏠 Home (Run a Workflow)
# ---------------------
if menu == "Home":
    st.title("🏠 Run Workflow")

    workflow_files = []
    for root, _, files in os.walk(__workflow_path__):
        for file in files:
            if file.endswith((".yaml", ".yml")):
                relative_path = os.path.relpath(os.path.join(root, file), __workflow_path__)
                workflow_files.append(relative_path)
    workflow_files.sort()

    if "confirm_ready" not in st.session_state:
        st.session_state.confirm_ready = False
    if "last_selected_workflow" not in st.session_state:
        st.session_state.last_selected_workflow = None

    selected_file = st.selectbox("Select a Workflow to Run", workflow_files)

    if selected_file != st.session_state.last_selected_workflow:
        st.session_state.confirm_ready = False
        st.session_state.last_selected_workflow = selected_file

    workflow_path = os.path.join(__workflow_path__, selected_file)

    # Load YAML
    with open(workflow_path) as f:
        workflow_yaml = yaml.safe_load(f)

    st.markdown(f"### 🗂️ `{workflow_yaml.get('name', selected_file)}`")
    st.markdown(workflow_yaml.get("description", '*No description provided.*'))

    if st.button("🚀 Prepare to Run Workflow"):
        st.session_state.confirm_ready = True

    if st.session_state.confirm_ready:
        st.warning("⚠️ Are you sure you want to run this workflow?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm and Run"):
                with st.spinner("Running workflow..."):
                    result = run_workflow(workflow_path, streamlit_mode=True)
                    for step, output in result.items():
                        if step == "_execution_duration":
                            continue
                        st.subheader(f"Step: {step}")
                        st.text(output)
                st.session_state.confirm_ready = False
                if "_execution_duration" in result:
                    st.success(f"✅ Workflow completed in {result['_execution_duration']} seconds.")
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.confirm_ready = False

# ---------------------
# 📄 Workflows (Read Workflow Files)
# ---------------------
elif menu == "Workflows":
    st.title("📄 Browse Workflow Files")

    workflow_files = []
    for root, _, files in os.walk(__workflow_path__):
        for file in files:
            if file.endswith((".yaml", ".yml")):
                relative_path = os.path.relpath(os.path.join(root, file), __workflow_path__)
                workflow_files.append(relative_path)

    selected_workflow = st.selectbox("Select a Workflow to Read", workflow_files)

    if selected_workflow:
        with open(os.path.join(__workflow_path__, selected_workflow)) as f:
            content = f.read()
        st.code(content, language="yaml")

# ---------------------
# 🧠 Agents
# ---------------------
elif menu == "Agents":
    st.title("🧠 Available Agents (Grouped by Type)")

    # Prepare groups
    agent_groups = {
        "AI": [],
        "AI-Image": [],
        "AI-Audio": [],
        "Git": [],
        "RAG": [],
        "Utility": [],
    }

    for agent_name, agent_info in AGENT_CATALOG.items():
        agent_type = agent_info.get("type", "Utility")  # Default fallback
        agent_groups.setdefault(agent_type, []).append((agent_name, agent_info))

    # Display groups
    for group_name, agents in agent_groups.items():
        if not agents:
            continue

        with st.expander(f"📂 {group_name} Agents ({len(agents)})", expanded=True):
            for agent_name, agent_info in agents:
                st.subheader(f"🔹 {agent_name}")
                st.markdown(f"{agent_info['short_description']}")

# ---------------------
# 🧠 Models
# ---------------------
elif menu == "Models":
    st.title("🧠 Supported Models")

    for model_name, model_info in MODEL_CATALOG.items():
        st.subheader(f"🔹 {model_name}")
        st.markdown(f"{model_info['description']}")
# ---------------------
# ⚙️ Config
# ---------------------
elif menu == "Config":
    st.title("⚙️ Configuration Info")

    st.markdown(f"""
    - **App Version:** `{__version__}`
    - **Workflow Path:** `{__workflow_path__}`
    - **Active Models/Agents:** See respective pages.
    """)

# ---------------------
# 📄 Templates
# ---------------------
elif menu == "Templates":
    st.title("📄 Available Prompt Templates")

    templates_dir = "prompts"
    templates = []
    for root, _, files in os.walk(templates_dir):
        for file in files:
            if file.endswith(".txt"):
                templates.append(os.path.relpath(os.path.join(root, file), templates_dir))

    selected_template = st.selectbox("Select a Template File", templates)

    if selected_template:
        with open(os.path.join(templates_dir, selected_template)) as f:
            content = f.read()
        st.code(content, language="markdown")

# ---------------------
# 📚 Docs (Readme)
# ---------------------
elif menu == "Docs":
    st.title("📚 Documentation (README)")

    readme_path = "README.md"

    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            readme_content = f.read()
        st.markdown(readme_content)
    else:
        st.warning("README.md not found.")
