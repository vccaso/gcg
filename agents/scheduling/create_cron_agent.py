import os
import yaml
from agents.base import BaseAgent

class CreateCronJobAgent(BaseAgent):
    def __init__(self, schedule_path="configs/workflow_schedules.yaml"):
        super().__init__()
        self.schedule_path = schedule_path

    def run(self, name, workflow, cron):
        os.makedirs(os.path.dirname(self.schedule_path), exist_ok=True)

        # Load existing schedules
        if os.path.exists(self.schedule_path):
            with open(self.schedule_path, "r") as f:
                data = yaml.safe_load(f) or {}
        else:
            data = {}

        if "schedules" not in data:
            data["schedules"] = []

        # Check for duplicate name
        for job in data["schedules"]:
            if job.get("name") == name:
                return {"status": "error", "message": f"Job '{name}' already exists."}

        # Add new job
        data["schedules"].append({
            "name": name,
            "workflow": workflow,
            "cron": cron
        })

        # Save back
        with open(self.schedule_path, "w") as f:
            yaml.safe_dump(data, f)

        return {"status": "success", "message": f"Scheduled job '{name}' for {cron}"}
