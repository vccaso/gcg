# agents/image_analysis_agent.py
import os
from models.openai.model_gpt_image_1 import ModelGptImage1
from utils.printer import Printer

class ImageAnalysisAgent:
    def __init__(self, model: ModelGptImage1):
        if not isinstance(model, ModelGptImage1):
            raise ValueError("Model must be an instance of ModelGptImage1")
        self.model = model

    def run(self, prompt: str, image_path: str):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        Printer.info(f"🔍 Analyzing image: {image_path} with prompt: '{prompt}'")
        analysis = self.model.analyze_image(prompt, image_path)
        Printer.success("✅ Analysis complete")

        return {
            "status": "success",
            "image_path": image_path,
            "analysis": analysis
        }
