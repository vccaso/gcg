from agents.base import BaseAgent
from models.modelbase import ModelBase

class ScriptFeedbackValidatorAgent(BaseAgent):
    def __init__(self, llm: ModelBase, prompt_template: str):
        self.llm = llm
        self.prompt_template = prompt_template

    def run(self, **kwargs):
        script = kwargs["script"]
        topic = kwargs.get("topic", "this topic")

        formatted_prompt = self.prompt_template.format(script=script, topic=topic)
        response = self.llm.get_response(formatted_prompt)

        try:
            sections = response.split("===\n")
            if len(sections) < 3:
                raise ValueError("Response does not contain 3 expected sections.")

            recommendations = sections[0].strip()
            score_line = sections[1].strip()
            improved_prompt = sections[2].strip()

            score = int("".join(filter(str.isdigit, score_line.splitlines()[0])))

            return {
                "status": "pass" if score >= 60 else "fail",
                "recommendations": recommendations,
                "score": score,
                "improved_prompt": improved_prompt
            }

        except Exception as e:
            raise ValueError(f"Failed to parse response from LLM: {e}")
