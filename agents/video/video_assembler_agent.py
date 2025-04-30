from moviepy.editor import ImageClip, AudioFileClip
from agents.base import BaseAgent  

import os

class VideoAssemblerAgent(BaseAgent):
    def run(self, image_path, audio_path, output_video_path, duration=None):
        if not os.path.exists(image_path):
            return {"error": f"Image not found: {image_path}"}
        if not os.path.exists(audio_path):
            return {"error": f"Audio not found: {audio_path}"}

        audio_clip = AudioFileClip(audio_path)
        image_clip = ImageClip(image_path).set_duration(duration or audio_clip.duration)
        image_clip = image_clip.set_audio(audio_clip)
        image_clip = image_clip.resize(height=720)  # Resize for YouTube compatibility

        try:
            image_clip.write_videofile(output_video_path, fps=24, codec='libx264', audio_codec='aac')
            return {"status": "success", "output_video": output_video_path}
        except Exception as e:
            return {"error": str(e)}
