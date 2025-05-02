import os
import re
from models.modelbase import ModelBase
from utils.printer import Printer
from utils.gocodeutil import GoCodeUtil
from config import debug
import openai
import requests

class Dalle2Agent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def generate_image(self, prompt: str, size="256x256") -> dict:
        """
        Generates an image using DALL·E 3 from the given prompt.

        Parameters:
        - prompt: Description of the image
        - size: Image size (256x256, 512x512 , or 1024x1024)

        Returns:
        - A dictionary with URL and optional metadata
        """
        try:
            response = openai.images.generate(
                model="dall-e-2",
                prompt=prompt,
                n=1,
                size=size,
                response_format="url"
            )
            image_data = response.data[0]
            return {
                "url": image_data.url,
                "revised_prompt": image_data.revised_prompt if hasattr(image_data, "revised_prompt") else prompt
            }
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return {"error": str(e)}
