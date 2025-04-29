# api/main.py

import os
import sys
from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
import uvicorn
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orchestrator_core import run_workflow

# 💡 App Initialization
app = FastAPI(title="GCG API", description="Run workflows via API", version="1.0")

# 🔒 Simple API Key for Authentication
API_KEY = os.getenv("GCG_API_KEY", "changeme")

# 🔑 Dependency to Verify API Key
async def verify_api_key(request: Request):
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized. Invalid API Key.")

# 📚 Request Model
class WorkflowRequest(BaseModel):
    workflow_file: str

class InlineWorkflowRequest(BaseModel):
    workflow_yaml: str

# 🔄 Endpoint to Run a Workflow (by file)
@app.post("/workflow", dependencies=[Depends(verify_api_key)])
def run_workflow_endpoint(request: WorkflowRequest):
    workflow_path = os.path.join("workflows", request.workflow_file)

    if not os.path.exists(workflow_path):
        raise HTTPException(status_code=404, detail=f"Workflow '{request.workflow_file}' not found.")

    try:
        result = run_workflow(workflow_path, streamlit_mode=False)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")

# 🔍 Endpoint to List Available Workflows
@app.get("/workflow", dependencies=[Depends(verify_api_key)])
def list_workflows():
    base_dir = "workflows"
    available = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                rel_path = os.path.relpath(os.path.join(root, file), base_dir)
                available.append(rel_path)
    return {"workflows": sorted(available)}

# 📃 Endpoint to Fetch Workflow Content
@app.get("/workflow/{name}", dependencies=[Depends(verify_api_key)])
def get_workflow_content(name: str):
    workflow_path = os.path.join("workflows", name)
    if not os.path.exists(workflow_path):
        raise HTTPException(status_code=404, detail=f"Workflow '{name}' not found.")

    try:
        with open(workflow_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"name": name, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading workflow: {str(e)}")

# ✅ Run a workflow from raw YAML input
@app.post("/workflow/inline", dependencies=[Depends(verify_api_key)])
def run_inline_workflow(request: InlineWorkflowRequest):
    try:
        workflow_dict = yaml.safe_load(request.workflow_yaml)
        result = run_workflow_from_yaml(workflow_dict)
        return {"status": "success", "result": result}
    except yaml.YAMLError as ye:
        raise HTTPException(status_code=400, detail=f"Invalid YAML: {ye}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")


# 🛠️ Local running support (optional)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

