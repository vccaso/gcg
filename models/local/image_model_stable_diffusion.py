from models.image_model_base import ImageModelBase
import requests
import os

class ImageModelStableDiffusion(ImageModelBase):
    def __init__(self, hf_token=None, api_url=None):
        self.hf_token = hf_token or os.getenv("HUGGINGFACE_TOKEN")
        self.api_url = api_url or "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
        if not self.hf_token:
            raise ValueError("Missing Hugging Face token")

    def generate_image(self, prompt: str, output_path: str):
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Accept": "application/json"
        }

        payload = {
            "inputs": prompt,
        }

        print(f"🔮 Generating image from prompt: {prompt}")
        response = requests.post(self.api_url, headers=headers, json=payload)

        if response.status_code != 200:
            raise RuntimeError(f"Stable Diffusion API error: {response.status_code} - {response.text}")

        image_data = response.content
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_data)
        print(f"✅ Image saved to {output_path}")



# 🧪 Example Usage

# model = ImageModelStableDiffusion(hf_token="your-token-here")
# model.generate_image("a futuristic cityscape at sunset", "output/image.png")