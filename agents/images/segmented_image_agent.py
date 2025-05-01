import os
import openai
import requests
from agents.base import BaseAgent
from utils.yaml_util import parse_and_validate_yaml
from schemas.structured_script_schema import STRUCTURED_SCRIPT_SCHEMA

class SegmentedImageAgent(BaseAgent):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def run(self, **kwargs):
        raw_sections = kwargs["text_sections"]

        # ✅ Parse YAML or dict
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

        output_dir = kwargs.get("output_dir", "workspace/images")
        prefix = kwargs.get("filename_prefix", "image")
        model = kwargs.get("model", "dall-e-3")

        os.makedirs(output_dir, exist_ok=True)
        downloaded_images = {}

        for key, section in text_sections.items():
            prompt = section.get("image_prompt", "")
            if not prompt:
                continue

            response = openai.images.generate(
                model=model,
                prompt=prompt,
                size="1024x1024",
                n=1
            )
            image_url = response.data[0].url

            # 🧲 Download image
            img_path = os.path.join(output_dir, f"{prefix}_{key}.png")
            try:
                img_data = requests.get(image_url).content
                with open(img_path, "wb") as f:
                    f.write(img_data)
                downloaded_images[key] = img_path
            except Exception as e:
                downloaded_images[key] = f"Download failed: {e}"

        return {
            "status": "success",
            "images": downloaded_images
        }
