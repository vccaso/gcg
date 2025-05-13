import requests
from agents.base import BaseAgent

class WebhookAgent(BaseAgent):
    def run(self, **kwargs):
        url = kwargs.get("url")
        payload = kwargs.get("payload", {})
        headers = kwargs.get("headers", {"Content-Type": "application/json"})

        if not url:
            return {"status": "error", "message": "Missing webhook URL."}

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            return {
                "status": "success" if response.ok else "error",
                "code": response.status_code,
                "response": response.text
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        