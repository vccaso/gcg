# models/audio/audio_model_coqui.py
import os
from TTS.api import TTS
from models.audio_model_base import AudioModelBase

class AudioModelCoqui(AudioModelBase):
    def __init__(self, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
        self.tts = TTS(model_name)

    def text_to_speech(self, text: str, output_path: str, voice: str = "", factor: float = 1.0) -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.tts.tts_to_file(text=text, file_path=output_path)
        return output_path

    def speech_to_text(self, audio_path: str) -> str:
        raise NotImplementedError("Speech-to-text is not supported for Coqui model.")
