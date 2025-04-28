import streamlit as st
import os
import yaml
from collections import defaultdict
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
    st.title("🤖 Available Agents")

    # Collect all unique tags
    all_tags = set()
    for agent_info in AGENT_CATALOG.values():
        all_tags.update(agent_info.get("tags", []))

    selected_tags = st.multiselect("🔎 Filter by Tags", sorted(list(all_tags)))

    st.divider()

    # Group agents by primary tag
    from collections import defaultdict
    grouped_agents = defaultdict(list)
    for agent_name, agent_info in AGENT_CATALOG.items():
        agent_tags = agent_info.get("tags", [])
        if not agent_tags:
            continue
        primary_tag = agent_tags[0]
        grouped_agents[primary_tag].append((agent_name, agent_info))

    for group_name, agents in grouped_agents.items():
        with st.expander(f"📂 {group_name} Agents ({len(agents)})", expanded=True):
            for agent_name, agent_info in agents:
                agent_tags = agent_info.get("tags", [])

                # Apply filtering
                if selected_tags:
                    if not any(tag in agent_tags for tag in selected_tags):
                        continue

                st.subheader(f"🔹 {agent_name}")

                tags_str = ", ".join(f"[{tag}]" for tag in agent_tags)
                st.markdown(f"**Tags:** {tags_str}")

                st.markdown(agent_info["short_description"])
                st.divider()

# ---------------------
# 🧠 Models
# ---------------------
elif menu == "Models":
    st.title("🧠 Supported Models")

    # Collect all unique tags
    all_tags = set()
    for model_info in MODEL_CATALOG.values():
        all_tags.update(model_info.get("tags", []))

    selected_tags = st.multiselect("🔎 Filter by Tags", sorted(list(all_tags)))

    st.divider()

    # Group models by their primary tag
    grouped_models = defaultdict(list)
    for model_name, model_info in MODEL_CATALOG.items():
        model_tags = model_info.get("tags", [])
        if not model_tags:
            continue

        primary_tag = model_tags[0]  # First tag is the grouping key
        grouped_models[primary_tag].append((model_name, model_info))

    # Display models grouped
    for group_name, models in grouped_models.items():
        with st.expander(f"📂 {group_name} Models ({len(models)})", expanded=True):
            for model_name, model_info in models:
                model_tags = model_info.get("tags", [])

                # ✅ Filter each model by all selected tags
                if selected_tags:
                    if not any(tag in model_tags for tag in selected_tags):
                        continue  # Skip if no matching tag

                st.subheader(f"🔹 {model_name}")

                tags_str = ", ".join(f"[{tag}]" for tag in model_tags)
                st.markdown(f"**Tags:** {tags_str}")

                st.markdown(model_info["short_description"])
                st.divider()
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
