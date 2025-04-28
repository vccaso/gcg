import os
import re
from models.modelbase import ModelBase
from utils.printer import Printer
from utils.gocodeutil import GoCodeUtil
from config import debug
import openai
import requests

            

class AudioAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def text_to_speech(self, text: str, voice="alloy", model="tts-1", output_path="output/audio.wav") -> str:
        """
        Converts text to speech using OpenAI's TTS model and saves the audio file.
        """
        response = openai.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        response.stream_to_file(output_path)
        return output_path

    def speech_to_text(self, audio_file_path: str, model="whisper-1") -> str:
        """
        Transcribes an audio file to text using Whisper.
        """
        with open(audio_file_path, "rb") as f:
            transcript = openai.audio.transcriptions.create(
                model=model,
                file=f
            )
        return transcript.text

    def run(self, **kwargs):
        mode = kwargs.get("mode")

        if mode == "tts":
            return self.text_to_speech(
                text=kwargs["text"],
                voice=kwargs.get("voice", "alloy"),
                model=kwargs.get("model", "tts-1"),
                output_path=kwargs.get("output_path", "output/audio.wav")
            )

        elif mode == "stt":
            return self.speech_to_text(
                audio_file_path=kwargs["audio_file_path"],
                model=kwargs.get("model", "whisper-1")
            )

        else:
            raise ValueError("Invalid mode. Use 'tts' or 'stt'.")
