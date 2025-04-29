# api/main.py

import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orchestrator_core import run_workflow


# 💡 App Initialization
app = FastAPI(title="GCG API", description="Run workflows via API", version="1.0")

# 📚 Request Model
class WorkflowRequest(BaseModel):
    workflow_file: str

# 🔄 Endpoint to Run a Workflow
@app.post("/run-workflow")
def run_workflow_endpoint(request: WorkflowRequest):
    workflow_path = os.path.join("workflows", request.workflow_file)

    if not os.path.exists(workflow_path):
        raise HTTPException(status_code=404, detail=f"Workflow '{request.workflow_file}' not found.")

    try:
        result = run_workflow(workflow_path, streamlit_mode=False)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")

# 🛠️ Local running support (optional)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)