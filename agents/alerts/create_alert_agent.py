import os
import yaml
from agents.base import BaseAgent

class CreateAlertAgent(BaseAgent):
    def __init__(self, alert_path="configs/alert_rules.yaml"):
        super().__init__()
        self.alert_path = alert_path

    def run(self, name, condition, interval, actions):
        os.makedirs(os.path.dirname(self.alert_path), exist_ok=True)

        if os.path.exists(self.alert_path):
            with open(self.alert_path, "r") as f:
                data = yaml.safe_load(f) or {}
        else:
            data = {}

        if "alerts" not in data:
            data["alerts"] = []

        for alert in data["alerts"]:
            if alert.get("name") == name:
                return {"status": "error", "message": f"Alert '{name}' already exists."}

        data["alerts"].append({
            "name": name,
            "condition": condition,
            "interval": interval,
            "actions": actions
        })

        with open(self.alert_path, "w") as f:
            yaml.safe_dump(data, f)

        return {"status": "success", "message": f"Created alert '{name}' with interval {interval}"}
