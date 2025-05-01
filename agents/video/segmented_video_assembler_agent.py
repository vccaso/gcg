import os
import glob
from agents.base import BaseAgent
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

class SegmentedVideoAssemblerAgent(BaseAgent):
    def run(self, **kwargs):
        audio_dir = kwargs["audio_dir"]     # e.g. workspace/video01/audio/segments04
        image_dir = kwargs["image_dir"]     # e.g. workspace/video01/images/segments04
        output_path = kwargs.get("output_path", "workspace/videos/final_video.mp4")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        clips = []

        for section in ["intro", "scene1", "scene2", "scene3", "conclusion"]:
            audio_glob = glob.glob(os.path.join(audio_dir, f"*{section}.wav"))
            image_glob = glob.glob(os.path.join(image_dir, f"*{section}.png"))

            if not audio_glob or not image_glob:
                print(f"⚠️ Skipping section '{section}' — audio or image missing.")
                continue

            audio_path = audio_glob[0]
            image_path = image_glob[0]

            audio = AudioFileClip(audio_path)
            image = ImageClip(image_path).set_duration(audio.duration)
            image = image.set_audio(audio).resize(height=720).set_fps(24)

            clips.append(image)

        if not clips:
            raise ValueError("No valid media found for any section.")

        final = concatenate_videoclips(clips, method="compose")
        final.write_videofile(output_path, codec="libx264", audio_codec="aac")

        return {
            "status": "success",
            "video_path": output_path
        }
