import json
import re
from jsonschema import validate, ValidationError
import yaml

STRUCTURED_SCRIPT_SCHEMA = {
    "type": "object",
    "required": ["intro", "scene1", "scene2", "scene3", "conclusion"],
    "properties": {
        "intro": {"type": "string"},
        "scene1": {"type": "string"},
        "scene2": {"type": "string"},
        "scene3": {"type": "string"},
        "conclusion": {"type": "string"},
    },
    "additionalProperties": False
}

def escape_inner_quotes(json_str):
    # Avoid quotes in keys (before the colon) and escape quotes in values only
    return re.sub(r'(?<=:\s*)"([^"]*?)"(?=\s*[},])', lambda m: m.group(0).replace('"', '\\"'), json_str)

def extract_and_validate_json(raw_input: str, schema: dict) -> dict:
    """
    Extracts a JSON object from a raw string, cleans it, and validates it against a schema.

    Args:
        raw_input (str): The raw string containing the JSON object.
        schema (dict): The JSON schema to validate against.

    Returns:
        dict: The validated JSON object.

    Raises:
        ValueError: If extraction, parsing, or validation fails.
    """
     # Extract first brace block
    start = raw_input.find("{")
    end = raw_input.rfind("}") + 1
    if start == -1 or end <= start:
        raise ValueError("No JSON object found in the input string.")
    
    json_str = raw_input[start:end]

    # Fix missing commas between fields (e.g. }"scene2": → },"scene2":
    json_str = re.sub(r'"\s*"\s*:', '", "', json_str)  # close unquoted strings
    json_str = re.sub(r'(?<="[^"]+)"\s*(?=")', '",', json_str)  # insert comma

    # Fix double-quote imbalance (e.g. open quote but not closed)
    open_quotes = json_str.count('"')
    if open_quotes % 2 != 0:
        json_str += '"'

    # Balance braces
    open_braces = json_str.count("{")
    close_braces = json_str.count("}")
    if open_braces > close_braces:
        json_str += "}" * (open_braces - close_braces)

    # Attempt parsing
    try:
        parsed = json.loads(json_str)
        validate(instance=parsed, schema=schema)
        return parsed
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Failed to fix and parse JSON: {e}")
    # try:
    #     # Step 1: Extract JSON object using regex
    #     match = re.search(r'({\s*"intro"\s*:.*?"conclusion"\s*:\s*".+?"\s*})', raw_input, re.DOTALL)
    #     if not match:
    #         # Try to grab best effort JSON if full pattern fails
    #         start = raw_input.find('{')
    #         end = raw_input.rfind('}') + 1
    #         if start != -1 and end > start:
    #             json_str = raw_input[start:end]
    #         else:
    #             raise ValueError("No JSON object found in the input string.")
    #     else:
    #         json_str = match.group(1)

    #     # Step 2: Balance braces
    #     open_braces = json_str.count('{')
    #     close_braces = json_str.count('}')
    #     if open_braces > close_braces:
    #         json_str += '}' * (open_braces - close_braces)

    #     # Step 3: Replace single quotes with double quotes
    #     json_str = re.sub(r"(?<!\\)'", '"', json_str)

    #     # Step 4: Escape control characters
    #     json_str = re.sub(r'[\x00-\x1F]+', '', json_str)
    #     json_str = escape_inner_quotes(json_str)

    #     print("🧪 Cleaned JSON to parse:\n", json_str)
    #     # Step 5: Parse JSON
    #     data = json.loads(json_str)

    #     # Step 6: Validate against schema
    #     validate(instance=data, schema=schema)

    #     return data

    # except json.JSONDecodeError as e:
    #     raise ValueError(f"JSON parsing error: {e}")
    # except ValidationError as e:
    #     raise ValueError(f"JSON validation error: {e}")



def extract_and_validate_yaml(raw_input: str, schema: dict) -> dict:
    try:
        # Extract YAML block (from first colon to end)
        start = raw_input.find("intro:")
        if start == -1:
            raise ValueError("No YAML starting with 'intro:' found.")
        yaml_block = raw_input[start:]

        # Parse YAML
        parsed = yaml.safe_load(yaml_block)

        # Validate
        validate(instance=parsed, schema=schema)
        return parsed
    except Exception as e:
        raise ValueError(f"Failed to parse YAML structured script: {e}")