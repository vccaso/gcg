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
        - ChatAgent:
            - General-purpose conversational AI.
            - Ideal for brainstorming, answering questions, writing content, or summarization.
            - Best choice for unstructured tasks or idea generation.

        - GoCRUDAgent:
            - Full-stack Go CRUD code generator (Model + Data + API + Routes).
            - Best for quickly scaffolding complete backend services.

        - GoCRUDModelAgent:
            - Generates Go model structs only.
            - Adds JSON tags, database tags, validation, and Swagger annotations.

        - GoCRUDDataAgent:
            - Generates only the SQL-based data access layer (DAO) for Go.
            - Implements Create, Read, Update, Delete (CRUD) functions with real SQL.

        - GoSwaggerAgent:
            - Generates Swagger/OpenAPI documentation for Go services.
            - Useful for API documentation and external integration.

        - AngularAppAgent:
            - Creates Angular frontend application code.
            - Can scaffold features, components, services, and routing.

        - Dalle3Agent:
            - Generates high-quality images from text prompts using DALL·E 3.
            - Ideal for marketing visuals, UI mockups, creative content.

        - AudioAgent:
            - Handles both:
            - Text-to-Speech (TTS): Convert text into audio files
            - Speech-to-Text (STT): Transcribe audio files into text
            - Useful for voice messages, podcasts, audio UIs.

        - SaveToFileAgent:
            - Allows saving generated content, prompts, or outputs into files.
            - Helpful for logging, exporting, or audit purposes.

        - GitHubCreateBranchAgent:
            - Creates a new Git branch locally.
            - Can be used for feature, hotfix, or release branch creation.

        - GitHubPRAgent:
            - Automates creating a Pull Request (PR) on GitHub.
            - Useful for code review and collaboration workflows.

        - GitHubCommitAgent:
            - Creates a commit in a local Git repository.
            - Supports customizable commit messages.

        - GitHubCheckoutBranchAgent:
            - Checks out a Git branch locally.
            - If the branch doesn't exist, attempts to create and track it from `origin`.

        - GitHubCloneOrUpdateRepoAgent:
            - Clones a GitHub repository if missing or updates it (pull) if already cloned.
            - Ensures local repositories are always synchronized.

    """.strip()

    def get_model_description(self):
        return """
        - ModelOllama:
            - Local model running on your machine.
            - Free to use but slower than cloud models.
            - Good for basic chat, small tasks, and offline use.

        - ModelDeepSeekCoder67:
            - Specialized coding model trained on 2 trillion code + natural language tokens.
            - Excels at generating Go, Python, JavaScript, SQL, and complex algorithms.
            - Best choice for large, accurate code generation tasks.

        - ModelGpt4Turbo:
            - Most powerful general model available.
            - Best for structured code generation, logic-heavy workflows, and complex planning.
            - Highly reliable but higher API cost.

        - ModelGpt35Turbo:
            - Fast and cost-efficient.
            - Good for lightweight code tasks, brainstorming, chatbots, or simple CRUD generation.
            - Slightly less accurate on complex tasks.

        - ModelDalle3:
            - Advanced model for generating high-quality images from text prompts.
            - Ideal for creating marketing banners, UI designs, visual content.

        - ModelTTS1:
            - Text-to-speech model.
            - Converts text into high-fidelity spoken audio (multiple voices available).
            - Use for welcome messages, voice notifications, or audio content generation.

        - ModelWhisper:
            - Automatic speech recognition (ASR) model.
            - Transcribes audio recordings (.mp3, .wav) into text.
            - Best for meeting notes, interviews, podcasts, or audio summarization.
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
