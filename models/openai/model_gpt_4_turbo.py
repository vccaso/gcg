import os
from abc import ABC, abstractmethod
import openai  # pip install openai
from models.modelbase import ModelBase
from utils.printer import Printer


class ModelGpt4Turbo(ModelBase):
    def __init__(self, temperature=0.2):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.temperature=temperature
        super().__init__(openai.api_key)

    def get_response(self, prompt):
        """
        Sends the prompt to GPT-4 via OpenAI API and returns the response.
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=1500,
            )
        except Exception as e:
            Printer.error(f"Error calling OpenAI API: {e}")
            return

        return response.choices[0].message.content.strip()
    

