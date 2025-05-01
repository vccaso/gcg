import os
import openai
from agents.base import BaseAgent
from utils.yaml_util import parse_and_validate_yaml
from schemas.structured_script_schema import STRUCTURED_SCRIPT_SCHEMA

class SegmentedAudioAgent(BaseAgent):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def run(self, **kwargs):
        raw_sections = kwargs["text_sections"]

        # ✅ Parse YAML string or validate dict directly
        if isinstance(raw_sections, str):
            try:
                start = raw_sections.find("intro:")
                if start == -1:
                    raise ValueError("YAML must start with 'intro:'")
                yaml_block = raw_sections[start:]
                text_sections = parse_and_validate_yaml(yaml_block, STRUCTURED_SCRIPT_SCHEMA)
            except Exception as e:
                raise ValueError(f"Failed to parse YAML structured script: {e}")
        elif isinstance(raw_sections, dict):
            text_sections = parse_and_validate_yaml(raw_sections, STRUCTURED_SCRIPT_SCHEMA)
        else:
            raise TypeError("'text_sections' must be a dict or YAML string")

        # 🧠 Generate audio per section
        output_dir = kwargs.get("output_dir", "workspace/audio")
        prefix = kwargs.get("filename_prefix", "segment")
        voice = kwargs.get("voice", "alloy")
        model = kwargs.get("model", "tts-1")

        os.makedirs(output_dir, exist_ok=True)
        generated_files = {}

        for key, text in text_sections.items():
            path = os.path.join(output_dir, f"{prefix}_{key}.wav")
            response = openai.audio.speech.create(
                model=model,
                voice=voice,
                input=text
            )
            response.stream_to_file(path)
            generated_files[key] = path

        return {
            "status": "success",
            "files": generated_files
        }
