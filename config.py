# config.py

import yaml
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")

with open(CONFIG_FILE, "r") as f:
    _config = yaml.safe_load(f)

__version__ = _config.get("version", "0.0.0")
__app_name__ = _config.get("app_name", "AI Orchestrator")
__workflow_path__ = _config.get("workflow_path", "workflows")
debug = _config.get("debug", False)
