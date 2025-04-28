import os
import re
from models.modelbase import ModelBase
from utils.printer import Printer
from config import debug
import openai
import requests


class Dalle3Agent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def generate_image(self, prompt: str, image_path: str = None, size="1024x1024", quality="standard", style="vivid") -> dict:
        """
        Generates an image using DALL·E 3 and optionally saves it to disk.

        Parameters:
        - prompt: Image description
        - image_path: Local path to save the image (e.g., output/image.png)
        - size: Image size for DALL·E 3
        - quality: 'standard' or 'hd'
        - style: 'vivid' or 'natural'

        Returns:
        - A dictionary with image URL, saved path (if any), and revised prompt
        """
        try:
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size=size,
                quality=quality,
                style=style
            )
            image_data = response.data[0]
            image_url = image_data.url
            revised_prompt = getattr(image_data, "revised_prompt", prompt)

            result = {"url": image_url, "revised_prompt": revised_prompt}

            if image_path:
                self._download_image(image_url, image_path)
                result["saved_to"] = image_path

            return result

        except Exception as e:
            print(f"❌ Error generating or downloading image: {e}")
            return {"error": str(e)}

    def _download_image(self, url: str, path: str):
        """
        Downloads image from a URL and saves to local disk.
        """
        response = requests.get(url)
        response.raise_for_status()

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(response.content)
