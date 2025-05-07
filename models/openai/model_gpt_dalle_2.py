import os
import openai
from models.image_model_base import ImageModelBase
import requests

class ModelDalle2(ImageModelBase):
    """
    DALL·E 2 image generation model using OpenAI's API.
    """
        
    def __init__(self, temperature=0.2, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.temperature = temperature
        openai.api_key = self.api_key

    def generate_image(self, prompt: str, output_path: str, size="256x256") -> str:

        """
        Generates an image using DALL·E 2 from the given prompt.

        Args:
            prompt (str): Description of the image to generate.
            size (str): Image resolution. One of: '256x256', '512x512', '1024x1024'.

        Returns:
            dict: Dictionary with 'url' and optionally 'revised_prompt', or an 'error'.
        """
        valid_sizes = {"256x256", "512x512", "1024x1024"}
        if size not in valid_sizes:
            return {"error": f"Invalid size '{size}'. Must be one of {valid_sizes}"}

        try:
            response = openai.images.generate(
                model="dall-e-2",
                prompt=prompt,
                n=1,
                size=size,
                response_format="url"
            )
            image_data = response.data[0]
            # Save to file
            image_data = requests.get(image_data.url).content
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(image_data)
            return output_path
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return {"error": str(e)}
