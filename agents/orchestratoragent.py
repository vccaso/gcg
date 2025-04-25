import yaml
import os

class OrchestratorAgent:
    def __init__(self, llm, prompt_template: str = None):
        self.llm = llm
        self.prompt_template = prompt_template or "You are a workflow planner..."
    

    def generate_prompt(self, user_request: str) -> str:
        p = self.prompt_template.format(
            request=user_request,
            agents_description=self.get_agent_description(),
            models_description=self.get_model_description()
        )
        return p

    def get_agent_description(self):
        return """
    - ChatAgent: General-purpose language model for Q&A and content generation.
    - GoCRUDAgent: Full-stack Go CRUD generator.
    - GoCRUDModelAgent: Only generates Go model structs.
    - GoCRUDDataAgent: Only generates SQL-based data layer code.
    - GoSwaggerAgent: Swagger/OpenAPI doc generator.
    - Dalle3Agent: DALL·E 3 image generator.
    - AudioAgent: Text-to-speech and speech-to-text audio processor.
    """.strip()

    def get_model_description(self):
        return """
    - ModelGpt4Turbo: Best for structured code generation and logic-heavy tasks.
    - ModelGpt35Turbo: Fast, lower cost, suitable for simple code tasks.
    - ModelDalle3: For generating images.
    - ModelTTS1: For generating speech audio from text.
    - ModelWhisper: For transcribing audio to text.
    """.strip()

    def run(self, request: str, save_path: str = "workflows/wf_generated.yaml") -> dict:


        final_prompt = self.generate_prompt(request)
        print(f"final prompt: {final_prompt}")
        workflow_yaml = self.llm.get_response(final_prompt).strip()

        # Clean markdown code block if present
        if workflow_yaml.startswith("```yaml"):
            workflow_yaml = workflow_yaml.replace("```yaml", "").strip()
        if workflow_yaml.endswith("```"):
            workflow_yaml = workflow_yaml[:-3].strip()

        # Save file
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(workflow_yaml)

        return {"path": save_path, "content": workflow_yaml}
