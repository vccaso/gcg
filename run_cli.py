import argparse
import os
from orchestrator_core import run_workflow
from config import __version__, __app_name__, __workflow_path__

parser = argparse.ArgumentParser(description="Run an AI agent workflow.")
parser.add_argument("--workflow", type=str, help="Path to the workflow file")
parser.add_argument("--version", action="store_true", help="Show version and exit")

args = parser.parse_args()

if args.version:
    print(f"{__app_name__} version {__version__}")
else:
    if not args.workflow:
        print("❌ Please provide a workflow file with --workflow <file>")
    else:
        workflow_path = os.path.join(__workflow_path__, args.workflow)
        run_workflow(workflow_path)
