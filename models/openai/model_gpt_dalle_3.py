# models/model_dalle3.py

import os
import openai
import requests
from models.image_model_base import ImageModelBase
from utils.printer import Printer

class ModelDalle3(ImageModelBase):
    """
    DALL·E 3 image generation model using OpenAI's API.
    """

    def __init__(self, temperature=0.2, openai_api_key=None):
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.temperature = temperature
        openai.api_key = self.api_key

    def generate_image(self, prompt: str, output_path: str, size: str = "1024x1024") -> str:
        """
        Generates an image from a text prompt using DALL·E 3 and saves it to the specified path.

        Args:
            prompt (str): The text description for the image.
            output_path (str): The file path to save the generated image.
            size (str): The desired resolution ('1024x1024', '1024x1792', or '1792x1024').

        Returns:
            str: The path to the saved image.
        """
        valid_sizes = {"1024x1024", "1024x1792", "1792x1024"}
        if size not in valid_sizes:
            raise ValueError(f"Invalid size '{size}'. Must be one of {valid_sizes}")

        try:
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size=size,
                response_format="url"
            )
            image_url = response.data[0].url

            image_data = requests.get(image_url).content
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(image_data)

            return output_path

        except Exception as e:
            Printer.error(f"Failed to generate image with DALL·E 3: {e}")
            raise
