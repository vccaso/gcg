# agents/planning/project_planner_agent.py
from typing import Optional, Dict, Any
from models.modelbase import ModelBase
from utils.printer import Printer 
from config import debug
import os


class ProjectPlannerAgent:
    """
    Generates a structured project plan using an LLM and a format-ready prompt template.

    Expected template placeholders (you can customize your template to use any subset):
      - objectives
      - scope
      - constraints
      - team
      - timeline
      - deliverables
      - context
      - notes

    Example template:
      \"\"\"
      You are a senior project planner.
      Using the following inputs, produce a detailed plan with milestones, risks, and RACI.

      Objectives: {objectives}
      Scope: {scope}
      Constraints: {constraints}
      Team: {team}
      Timeline: {timeline}
      Deliverables: {deliverables}
      Context: {context}
      Notes: {notes}
      \"\"\"
    """

    def __init__(self, llm: ModelBase, prompt_template: str):
        if not isinstance(llm, ModelBase):
            raise ValueError("LLM model must be an instance of ModelBase")
        self.llm = llm
        self.prompt_template = prompt_template

    def _ensure_dir(self, file_name: str) -> None:
        dir_path = os.path.dirname(file_name)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

    def run(
        self,
        *,
        objectives: str,
        scope: str = "",
        constraints: str = "",
        team: str = "",
        timeline: str = "",
        deliverables: str = "",
        context: str = "",
        notes: str = "",
        extra_placeholders: Optional[Dict[str, Any]] = None,
        save_to_file: bool = False,
        file_name: str = "project_plan_output.txt",
    ) -> Dict[str, str]:
        """
        Build the final prompt from provided fields, invoke the LLM, and optionally persist the response.

        Args:
            objectives: High-level goals and success criteria.
            scope: In-scope (and optionally out-of-scope) items.
            constraints: Budget, compliance, dependencies, assumptions, risks.
            team: Roles, skills, stakeholders.
            timeline: Dates, phases, milestones, cadence.
            deliverables: Tangible outputs/acceptance criteria.
            context: Background or environment details.
            notes: Any extra directions for tone/format.
            extra_placeholders: Dict for any additional template keys your prompt uses.
            save_to_file: Append the prompt/response to a file if True.
            file_name: Path to the file to append to.

        Returns:
            dict(status, details) — mirrors your existing agent interface.
        """
        # Assemble payload for template formatting
        payload = {
            "objectives": objectives,
            "scope": scope,
            "constraints": constraints,
            "team": team,
            "timeline": timeline,
            "deliverables": deliverables,
            "context": context,
            "notes": notes,
        }
        if extra_placeholders:
            payload.update(extra_placeholders)

        # Format prompt and handle missing placeholders clearly
        try:
            final_prompt = self.prompt_template.format(**payload)
        except KeyError as e:
            raise ValueError(f"Missing required placeholder in template: {e}")

        if debug:
            print(f"[🧠] Final Prompt:\n{final_prompt}\n")

        # Call the model
        response = self.llm.get_response(final_prompt)

        # Optional persistence
        if save_to_file:
            try:
                self._ensure_dir(file_name)
                with open(file_name, "a", encoding="utf-8") as f:
                    if debug:
                        f.write(f"Prompt:\n{final_prompt}\n\n")
                        f.write(f"Response:\n{response}\n")
                        f.write("-" * 40 + "\n")
                    else:
                        f.write(f"{response}\n\n")
            except Exception as e:
                print(f"⚠️ Failed to save response to file '{file_name}': {e}")
                return {"status": "Fail", "details": f"Failed to save response to file '{file_name}': {e}"}

        return {"status": "Success", "details": f"{response}"}
