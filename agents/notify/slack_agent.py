import requests
from agents.base import BaseAgent

class SlackAgent(BaseAgent):
    def run(self, **kwargs):
        webhook_url = kwargs.get("webhook_url")
        message = kwargs.get("message")

        if not webhook_url or not message:
            return {"status": "error", "details": "Missing webhook_url or message."}

        payload = {"text": message}

        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            return {
                "status": "success" if response.ok else "error",
                "code": response.status_code,
                "response": response.text
            }
        except Exception as e:
            return {"status": "error", "details": str(e)}
