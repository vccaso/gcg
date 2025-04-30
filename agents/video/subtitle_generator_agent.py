import os
import textwrap
from agents.base import BaseAgent

class SubtitleGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def format_time(self, seconds: float) -> str:
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

    def generate_srt(self, text: str, output_path: str, duration: float = 30.0, chars_per_segment: int = 60):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        chunks = textwrap.wrap(text, chars_per_segment)
        num_chunks = len(chunks)
        avg_segment_duration = duration / max(num_chunks, 1)

        lines = []
        for idx, chunk in enumerate(chunks, start=1):
            start_time = self.format_time(avg_segment_duration * (idx - 1))
            end_time = self.format_time(avg_segment_duration * idx)
            lines.append(f"{idx}")
            lines.append(f"{start_time} --> {end_time}")
            lines.append(chunk)
            lines.append("")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return {
            "status": "success",
            "srt_path": output_path,
            "segments": len(chunks)
        }

    def run(self, **kwargs):
        return self.generate_srt(
            text=kwargs["text"],
            output_path=kwargs["output_path"],
            duration=float(kwargs.get("duration", 30.0)),
            chars_per_segment=int(kwargs.get("chars_per_segment", 60))
        )
