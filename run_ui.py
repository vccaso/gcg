import streamlit as st
import os
import yaml
from orchestrator_core import run_workflow
from config import __version__, __app_name__, __workflow_path__

st.set_page_config(page_title=__app_name__, page_icon="🧠")
st.title(__app_name__)
st.markdown(f"<div style='text-align:right; color: gray;'>v{__version__}</div>", unsafe_allow_html=True)

workflow_files = [f for f in os.listdir(__workflow_path__) if f.endswith((".yaml", ".yml"))]

# Store state
if "confirm_ready" not in st.session_state:
    st.session_state.confirm_ready = False
if "last_selected_workflow" not in st.session_state:
    st.session_state.last_selected_workflow = None

# Workflow dropdown
selected_file = st.selectbox("Select a Workflow File", workflow_files)

# Reset confirmation if workflow changes
if selected_file != st.session_state.last_selected_workflow:
    st.session_state.confirm_ready = False
    st.session_state.last_selected_workflow = selected_file

workflow_path = os.path.join(__workflow_path__, selected_file)

# Load YAML content
with open(workflow_path) as f:
    workflow_yaml = yaml.safe_load(f)

st.markdown(f"### 🗂️ `{workflow_yaml.get('name')}`")
st.markdown(workflow_yaml.get("description", '*No description provided.*'))

# First button triggers confirmation state
if st.button("🚀 Prepare to Run Workflow"):
    st.session_state.confirm_ready = True

# Confirmation step
if st.session_state.confirm_ready:
    st.warning("⚠️ Are you sure you want to run this workflow?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirm and Run"):
            with st.spinner("Running workflow..."):
                result = run_workflow(workflow_path, streamlit_mode=True)
                st.success("✅ Workflow completed!")
                for step, output in result.items():
                    st.subheader(f"Step: {step}")
                    st.json(output)
            st.session_state.confirm_ready = False
    with col2:
        if st.button("❌ Cancel"):
            st.session_state.confirm_ready = False
