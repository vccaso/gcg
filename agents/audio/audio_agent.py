# agents/audio_agent.py
from models.audio_model_base import AudioModelBase

class AudioAgent:
    def __init__(self, model: AudioModelBase):
        if not isinstance(model, AudioModelBase):
            raise ValueError("Audio model must inherit from AudioModelBase.")
        self.model = model

    def run(self, **kwargs):
        mode = kwargs.get("mode")
        if mode == "tts":
            response = self.model.text_to_speech(
                text=kwargs["text"],
                output_path=kwargs.get("output_path", "output/audio.wav"),
                voice=kwargs.get("voice", ""),
                factor=kwargs.get("factor", 1.0)
            )
            return {"status": "Success", "details":response}
        elif mode == "stt":
            response = self.model.speech_to_text(kwargs["audio_file_path"])
            return {"status": "Success", "details":response}
        else:
            raise ValueError("Invalid mode. Use 'tts' or 'stt'.")


# import os
# import openai
# from moviepy.editor import AudioFileClip

# class AudioAgent:
#     def __init__(self, api_key=None):
#         self.api_key = api_key or os.getenv("OPENAI_API_KEY")
#         openai.api_key = self.api_key

#     def increase_volume(self, input_path, output_path, factor=1.0):
#         # Clamp volume factor between 0.1 and 3.0
#         factor = max(0.1, min(factor, 3.0))

#         audio = AudioFileClip(input_path)
#         louder = audio.volumex(factor)
#         louder.write_audiofile(output_path, codec='pcm_s16le')
#         audio.close()
#         louder.close()

#     def text_to_speech(self, text: str, voice="alloy", model="tts-1", output_path="output/audio.wav", factor=1.0) -> str:
#         response = openai.audio.speech.create(
#             model=model,
#             voice=voice,
#             input=text
#         )

#         os.makedirs(os.path.dirname(output_path), exist_ok=True)

#         if factor != 1.0:
#             dirname = os.path.dirname(output_path)
#             basename = os.path.basename(output_path)
#             tmp_path = os.path.join(dirname, f"tmp_{basename}")

#             response.stream_to_file(tmp_path)
#             self.increase_volume(tmp_path, output_path, factor)

#             try:
#                 os.remove(tmp_path)  # 🧹 Clean up temp file
#             except Exception as e:
#                 print(f"Warning: Failed to delete temp file: {e}")
#         else:
#             response.stream_to_file(output_path)

#         return output_path

#     def speech_to_text(self, audio_file_path: str, model="whisper-1") -> str:
#         with open(audio_file_path, "rb") as f:
#             transcript = openai.audio.transcriptions.create(model=model, file=f)
#         return transcript.text

#     def run(self, **kwargs):
#         mode = kwargs.get("mode")
#         if mode == "tts":
#             return self.text_to_speech(
#                 text=kwargs["text"],
#                 voice=kwargs.get("voice", "alloy"),
#                 model=kwargs.get("model", "tts-1"),
#                 output_path=kwargs.get("output_path", "output/audio.wav"),
#                 factor=kwargs.get("factor", 1.0)
#             )
#         elif mode == "stt":
#             return self.speech_to_text(
#                 audio_file_path=kwargs["audio_file_path"],
#                 model=kwargs.get("model", "whisper-1")
#             )
#         else:
#             raise ValueError("Invalid mode. Use 'tts' or 'stt'.")
