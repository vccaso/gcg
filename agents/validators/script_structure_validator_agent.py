import yaml
from agents.base_validator import ValidatorBaseAgent

class ScriptStructureValidatorAgent(ValidatorBaseAgent):
    def validate(self, input_data, expected_sections: list = None) -> dict:
        # Remove code block markers if present
        if isinstance(input_data, str):
            input_data = input_data.strip()
            if input_data.startswith("```yaml"):
                input_data = input_data[7:]  # strip '```yaml\n'
            if input_data.endswith("```"):
                input_data = input_data[:-3]

            try:
                input_data = yaml.safe_load(input_data)
            except yaml.YAMLError as e:
                return {"status": "fail", "reason": f"Invalid YAML: {e}"}

        if not isinstance(input_data, dict):
            return {"status": "fail", "reason": "Input is not a dictionary"}

        expected_sections = set(expected_sections or [])
        missing = expected_sections - input_data.keys()

        if missing:
            return {
                "status": "fail",
                "reason": f"Missing sections: {', '.join(sorted(missing))}"
            }

        return {"status": "pass"}
