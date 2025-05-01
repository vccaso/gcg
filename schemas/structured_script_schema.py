STRUCTURED_SCRIPT_SCHEMA_OLD = {
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


STRUCTURED_SCRIPT_SCHEMA = {
    "type": "object",
    "required": ["intro", "scene1", "scene2", "scene3", "conclusion"],
    "properties": {
        section: {
            "type": "object",
            "required": ["text", "image_prompt"],
            "properties": {
                "text": {"type": "string"},
                "image_prompt": {"type": "string"}
            },
            "additionalProperties": False
        } for section in ["intro", "scene1", "scene2", "scene3", "conclusion"]
    },
    "additionalProperties": False
}
