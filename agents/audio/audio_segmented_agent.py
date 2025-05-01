import os
from agents.base import BaseAgent
import openai
import json
import re

class SegmentedAudioAgent(BaseAgent):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def run(self, **kwargs):
        raw_sections = kwargs["text_sections"]

        if isinstance(raw_sections, str):
            try:
                # Step 1: Extract a block starting with "intro" and ending with "conclusion"
                match = re.search(r'({\s*"intro"[\s\S]*?"conclusion"\s*:\s*".+?"\s*})', raw_sections)
                if not match:
                    raise ValueError("No JSON object found in string.")
                cleaned = match.group(1)

                # Step 2: Balance curly braces if cutoff occurred
                open_braces = cleaned.count("{")
                close_braces = cleaned.count("}")
                if open_braces > close_braces:
                    cleaned += "}" * (open_braces - close_braces)

                # Step 3: Try to parse
                text_sections = json.loads(cleaned)

            except Exception as e:
                raise ValueError(f"Failed to parse 'text_sections': {e}")
        elif isinstance(raw_sections, dict):
            text_sections = raw_sections
        else:
            raise TypeError("'text_sections' must be a dict or JSON string")

    
        # text_sections = kwargs["text_sections"]  # Dict of key: text
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
