# models/audio/audio_model_openai.py
import os
import openai
from moviepy.editor import AudioFileClip
from models.audio_model_base import AudioModelBase

class AudioModelOpenAI(AudioModelBase):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def _increase_volume(self, path, factor):
        clip = AudioFileClip(path)
        louder = clip.volumex(factor)
        louder.write_audiofile(path, codec="pcm_s16le")
        clip.close()
        louder.close()

    def text_to_speech(self, text: str, output_path: str, voice="alloy", factor: float = 1.0) -> str:
        response = openai.audio.speech.create(model="tts-1", voice=voice, input=text)
        response.stream_to_file(output_path)

        if factor != 1.0:
            self._increase_volume(output_path, factor)

        return output_path

    def speech_to_text(self, audio_path: str) -> str:
        with open(audio_path, "rb") as f:
            transcript = openai.audio.transcriptions.create(model="whisper-1", file=f)
        return transcript.text
