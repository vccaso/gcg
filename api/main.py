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

# 🔄 Endpoint to Run a Workflow (with API Key Protection)
@app.post("/run-workflow", dependencies=[Depends(verify_api_key)])
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

