import os
import glob
from agents.base import BaseAgent
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

class SegmentedVideoAssemblerAgent(BaseAgent):

    def run(self, **kwargs):
        audio_dir = kwargs["audio_dir"]     # e.g. workspace/video01/audio/segments04
        image_dir = kwargs["image_dir"]     # e.g. workspace/video01/images/segments04
        output_path = kwargs.get("output_path", "workspace/videos/final_video.mp4")
        volume_factor = kwargs.get("factor", 1.0)

        # Clamp volume to avoid silence or clipping
        volume_factor = max(0.1, min(volume_factor, 3.0))

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        clips = []

        sections = [
            "intro", "background", "key_figures", "turning_point", "daily_life",
            "conflict", "resolution", "impact", "reflection", "outro"
        ]

        for section in sections:
            audio_glob = glob.glob(os.path.join(audio_dir, f"*{section}.wav"))
            image_glob = glob.glob(os.path.join(image_dir, f"*{section}.png"))

            if not audio_glob or not image_glob:
                print(f"⚠️ Skipping section '{section}' — audio or image missing.")
                continue

            audio_path = audio_glob[0]
            image_path = image_glob[0]

            audio = AudioFileClip(audio_path)
            if volume_factor != 1.0:
                audio = audio.volumex(volume_factor)

            image = (
                ImageClip(image_path)
                .set_duration(audio.duration)
                .set_audio(audio)
                .resize(height=720)
                .set_fps(24)
            )

            clips.append(image)

        if not clips:
            raise ValueError("No valid media found for any section.")

        final = concatenate_videoclips(clips, method="compose")
        final.write_videofile(output_path, codec="libx264", audio_codec="aac")

        return {
            "status": "success",
            "video_path": output_path
        }
