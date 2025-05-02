# agents/image_agent.py
import os
from models.image_model_base import ImageModelBase
from utils.printer import Printer  # Optional: for nicer CLI output

class ImageAgent:
    def __init__(self, model: ImageModelBase):
        if not isinstance(model, ImageModelBase):
            raise ValueError("model must inherit from ImageModelBase")
        self.model = model

    def run(self, prompt: str, output_path: str):
        """
        Generates an image from a prompt using the injected model and saves it to output_path.
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            Printer.info(f"🎨 Generating image for: '{prompt}'")
            self.model.generate_image(prompt, output_path)
            Printer.success(f"✅ Image saved to: {output_path}")
            return {"status": "success", "image_path": output_path}
        except Exception as e:
            Printer.error(f"❌ Image generation failed: {e}")
            return {"status": "error", "error": str(e)}

