import yaml
from jsonschema import validate, ValidationError

def strip_markdown_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```yaml"):
        text = text.replace("```yaml", "", 1).strip()
    if text.endswith("```"):
        text = text[:-3].strip()
    return text


def parse_and_validate_yaml(yaml_text, schema):
    if isinstance(yaml_text, dict):
        data = yaml_text  # already parsed
    else:
        # Strip code block fences if present
        if yaml_text.strip().startswith("```yaml"):
            yaml_text = yaml_text.strip().strip("`").split("yaml", 1)[-1].strip()
        elif yaml_text.strip().startswith("```"):
            yaml_text = yaml_text.strip().strip("`").split(None, 1)[-1].strip()

        try:
            data = yaml.safe_load(yaml_text)
        except Exception as e:
            raise ValueError(f"Invalid YAML: {e}")

    validate(instance=data, schema=schema)
    return data

def parse_and_validate_yaml_original(yaml_text: str, schema: dict) -> dict:
    try:
        data = yaml.safe_load(yaml_text)
        validate(instance=data, schema=schema)
        return data
    except Exception as e:
        raise ValueError(f"Invalid YAML: {e}")
