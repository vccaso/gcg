import yaml
from jsonschema import validate, ValidationError

def parse_and_validate_yaml(yaml_text: str, schema: dict) -> dict:
    try:
        data = yaml.safe_load(yaml_text)
        validate(instance=data, schema=schema)
        return data
    except Exception as e:
        raise ValueError(f"Invalid YAML: {e}")
