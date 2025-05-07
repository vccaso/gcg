import os
import openai
from base64 import b64encode
from models.image_model_base import ImageModelBase
from utils.printer import Printer

class ModelGptImage1(ImageModelBase):
    """
    GPT-4 Vision model for analyzing images with natural language prompts.
    """

    def __init__(self, temperature=0.2, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.temperature = temperature
        openai.api_key = self.api_key
        super().__init__()

    def generate_image(self, prompt: str, output_path: str) -> str:
        """
        Stub to comply with ImageModelBase. Not used in GPT-4 Vision.
        """
        raise NotImplementedError("ModelGptImage1 does not support image generation.")

    def analyze_image(self, prompt: str, image_path: str) -> str:
        """
        Analyzes an image using GPT-4 Vision.

        Args:
            prompt (str): The prompt/question to analyze the image.
            image_path (str): Path to the image file.

        Returns:
            str: Textual analysis result from the model.
        """
        try:
            with open(image_path, "rb") as img_file:
                encoded_image = b64encode(img_file.read()).decode("utf-8")

            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encoded_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                temperature=self.temperature,
                max_tokens=1500,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            Printer.error(f"Error querying GPT-4 Vision: {e}")
            return "❌ Failed to analyze image."
