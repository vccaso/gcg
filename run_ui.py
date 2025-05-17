import streamlit as st
import os
import yaml
from collections import defaultdict
from orchestrator_core import run_workflow
from models.model_registry import MODEL_CATALOG
from agents.agent_registry import AGENT_CATALOG
from api.api_catalog import API_CATALOG
from config import __version__, __app_name__, __workflow_path__
from chat import render_chat_page, render_chatv2_page
from graphviz import Digraph

st.set_page_config(page_title=__app_name__, page_icon="🧠")

CONFIG_SCHEDULE_PATH = "configs/workflow_schedules.yaml"
CONFIG_ALERT_PATH = "configs/alert_rules.yaml"
CRON_LOG = "logs/cron_history.log"
ALERT_LOG = "logs/alert_history.log"

# Sidebar menu
menu = st.sidebar.selectbox(
    "📂 Menu",
    ("Home", "Chatv2", "Workflows", "Agents", "Models", "Config", "Validate", "Templates", "API", "Docs", "Cronjobs", "Alerts", "Logs", "Chat")
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
                        if isinstance(output, dict) and "status" in output and "details" in output:
                            status_lower = output["status"].lower()
                            if status_lower == "success":
                                status_icon = "✅"
                            elif status_lower == "fail":
                                status_icon = "❌"
                            elif status_lower == "skipped":
                                status_icon = "⏭️"
                            else:
                                status_icon = "ℹ️"  # default for unknown statuses
                            st.markdown(f"{'&nbsp;' * 4}{status_icon} {output['details']}")
                        else:
                            st.text(output)
                st.session_state.confirm_ready = False
                if "_execution_duration" in result:
                    st.success(f"✅ Workflow completed in {result['_execution_duration']} seconds.")
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.confirm_ready = False

elif menu == "Chatv2":
    # This will render orchestrator_chat.py's logic
    render_chatv2_page()

elif menu == "Chat":
    # This will render orchestrator_chat.py's logic
    render_chat_page()

# ---------------------
# 📄 Workflows (Read Workflow Files)
# ---------------------
elif menu == "Workflows":
    st.title("📄 Browse Workflow Files")

    def get_step_colors(step_type):
        return {
            "ai": ("#66aaff", "#004488"),
            "validator": ("#b4e197", "#4b8544"),
            "utils": ("#ffe599", "#b8860b"),
            "git": ("#f4cccc", "#a61c00"),
            "rag": ("#d9d2e9", "#5e4b8b")
        }.get(step_type, ("#dddddd", "#666666"))  # Default

    def render_workflow_graph(workflow_dict):
        dot = Digraph()
        steps = workflow_dict.get("steps", [])
        # "BT" — Bottom to Top
        # "RL" — Right to Left
        rankdir = "LR" # "LR" — Left to Right
        if len(steps)>4:
            rankdir = "TB" # "TB" — Top to Bottom (default)
        dot.attr(   rankdir=rankdir, 
                    bgcolor="#99ccff",
                    margin="0.4",        # Default is 0.05; increase for more padding around the entire graph
                    pad="0.5",           # Extra padding outside the drawing
                    nodesep="0.8",       # Horizontal spacing between nodes
                    ranksep="0.8" )       # Vertical spacing between levels)  # top-to-bottom layouttransparent

        dot.attr(label=f"<<b>{workflow_dict.get('name', 'Workflow')}</b>>", fontsize="16", labelloc="t")
        for i, step in enumerate(steps):
            node_name = step["name"]
            agent = step.get("agent", "unknown")
            model = step.get("model", "N/A")
            step_type = step.get("type", "unknown")
            fillcolor, fontcolor = get_step_colors(step_type)

            style = "rounded,filled"
            if "when" in step:
                style += ",dashed"

            label = f"<<b>{i+1}. {node_name}</b><br/><br/><font point-size='10'>[{agent}]<br/>LLM:{model}</font>>"

            # 🧩 Custom node styling
            dot.node(
                node_name,
                label=label,
                tooltip=f"{step_type} | {agent} | {model}",
                shape="box",
                style=style,
                color="#aaaaff",
                fillcolor=fillcolor,
                fontname="Helvetica",
                fontcolor=fontcolor,
                fontsize="14",
            )

            if i > 0:
                prev_step = steps[i - 1]["name"]
                dot.edge(prev_step, node_name)

        return dot


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

        # Parse the YAML safely
        try:
            workflow_dict = yaml.safe_load(content)
            st.markdown("### 📈 Workflow Visualization")
            graph = render_workflow_graph(workflow_dict)
            st.graphviz_chart(graph)
            st.code(content, language="yaml")
        except Exception as e:
            st.error(f"Failed to parse and render workflow graph: {e}")


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

    # Prepare filtered agent list
    from collections import defaultdict
    grouped_agents = defaultdict(list)
    total_filtered = 0  # ✅ Counter for all visible agents

    for agent_name, agent_info in AGENT_CATALOG.items():
        agent_tags = agent_info.get("tags", [])
        if not agent_tags:
            continue
        if selected_tags and not any(tag in agent_tags for tag in selected_tags):
            continue  # ⛔ Skip agents not matching filter

        primary_tag = agent_tags[0]
        grouped_agents[primary_tag].append((agent_name, agent_info))
        total_filtered += 1  # ✅ Count valid agents

    st.markdown(f"**{total_filtered} agent(s) found**")
    st.divider()

    for group_name, agents in grouped_agents.items():
        with st.expander(f"📂 {group_name} Agents ({len(agents)})", expanded=True):
            for agent_name, agent_info in agents:
                st.subheader(f"🔹 {agent_name}")
                tags_str = ", ".join(f"[{tag}]" for tag in agent_info.get("tags", []))
                st.markdown(f"**Tags:** {tags_str}")
                st.markdown(agent_info["short_description"])
                st.divider()

# ---------------------
# 🧠 Models
# ---------------------
elif menu == "Models":
    st.title("🧠 Available Models")

    # Collect all unique tags
    all_tags = set()
    for model_info in MODEL_CATALOG.values():
        all_tags.update(model_info.get("tags", []))

    selected_tags = st.multiselect("🔎 Filter by Tags", sorted(list(all_tags)))

    # Prepare filtered model list
    from collections import defaultdict
    grouped_models = defaultdict(list)
    total_filtered = 0  # ✅ Counter for all visible models

    for model_name, model_info in MODEL_CATALOG.items():
        model_tags = model_info.get("tags", [])
        if not model_tags:
            continue
        if selected_tags and not any(tag in model_tags for tag in selected_tags):
            continue  # ⛔ Skip models not matching filter

        primary_tag = model_tags[0]
        grouped_models[primary_tag].append((model_name, model_info))
        total_filtered += 1  # ✅ Count valid models

    st.markdown(f"**{total_filtered} model(s) found**")
    st.divider()

    for group_name, models in grouped_models.items():
        with st.expander(f"📦 {group_name} Models ({len(models)})", expanded=True):
            for model_name, model_info in models:
                st.subheader(f"🧠 {model_name}")
                tags_str = ", ".join(f"[{tag}]" for tag in model_info.get("tags", []))
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
# 📄 Validate
# ---------------------
elif menu == "Validate":
    st.title("✅ Validate System Integrity")

    if st.button("🔍 Run Validation"):
        with st.spinner("Validating..."):
            from validate import main as run_validation
            run_validation()


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
        with open(os.path.join(templates_dir, selected_template), encoding="utf-8") as f:
            content = f.read()
        st.code(content, language="markdown")



# ---------------------
# 📄 API
# ---------------------
elif menu == "API":
    st.subheader("🔌 API Endpoints")
    st.markdown("Explore the available HTTP endpoints exposed by the GCG backend API.")
    for endpoint in API_CATALOG:
        st.subheader(f"`{endpoint['method']}` {endpoint['path']}")
        st.markdown(f"**Description:** {endpoint['description']}")
        if endpoint.get("auth"):
            st.markdown("**🔐 Requires API Key:** Yes")
        if endpoint.get("body"):
            st.markdown("**📦 Request Body Example:**")
            st.code(endpoint["body"], language="json")
        st.markdown("---")
# ---------------------
# 📚 Docs (Readme)
# ---------------------
elif menu == "Docs":
    st.title("📚 Documentation (README)")

    readme_path = "README.md"

    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
        st.markdown(readme_content)
    else:
        st.warning("README.md not found.")
# ---------------------
# 🧠 Models
# ---------------------
elif menu == "Cronjobs":
    st.header("⏰ Scheduled Cronjobs")
    if os.path.exists(CONFIG_SCHEDULE_PATH):
        with open(CONFIG_SCHEDULE_PATH) as f:
            data = yaml.safe_load(f)
            st.code(yaml.dump(data), language="yaml")
    else:
        st.warning("No cronjob configuration found.")

elif menu == "Alerts":
    st.header("🚨 Alert Rules")
    if os.path.exists(CONFIG_ALERT_PATH):
        with open(CONFIG_ALERT_PATH) as f:
            data = yaml.safe_load(f)
            st.code(yaml.dump(data), language="yaml")
    else:
        st.warning("No alert configuration found.")

elif menu == "Logs":
    st.header("📜 Logs")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Cron History")
        if os.path.exists(CRON_LOG):
            with open(CRON_LOG) as f:
                st.text(f.read())
        else:
            st.info("No cron log found.")

    with col2:
        st.subheader("Alert History")
        if os.path.exists(ALERT_LOG):
            with open(ALERT_LOG) as f:
                st.text(f.read())
        else:
            st.info("No alert log found.")
