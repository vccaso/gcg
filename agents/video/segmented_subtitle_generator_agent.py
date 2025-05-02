import os
from agents.base import BaseAgent
from moviepy.editor import AudioFileClip
from utils.yaml_util import parse_and_validate_yaml
from schemas.structured_script_schema import STRUCTURED_SCRIPT_SCHEMA

class SegmentedSubtitleGeneratorAgent(BaseAgent):
    def run(self, **kwargs):
        raw_sections = kwargs["text_sections"]
        audio_dir = kwargs["audio_dir"]
        prefix = kwargs.get("filename_prefix", "segment")
        output_path = kwargs.get("output_path", "workspace/videos/subtitles.srt")

        # ✅ Parse script input

        if isinstance(raw_sections, str):
            text_sections = parse_and_validate_yaml(raw_sections, STRUCTURED_SCRIPT_SCHEMA)
        elif isinstance(raw_sections, dict):
            text_sections = parse_and_validate_yaml(raw_sections, STRUCTURED_SCRIPT_SCHEMA)
        else:
            raise TypeError("'text_sections' must be a YAML string or dict")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        lines = []
        counter = 1
        current_time = 0.0

        def format_time(seconds):
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            s = int(seconds % 60)
            ms = int((seconds - int(seconds)) * 1000)
            return f"{h:02}:{m:02}:{s:02},{ms:03}"

        sections = list(text_sections.keys())
        for section in sections:
            section_data = text_sections.get(section)
            if not section_data or not isinstance(section_data, dict):
                continue

            audio_path = os.path.join(audio_dir, f"{prefix}_{section}.wav")
            if not os.path.exists(audio_path):
                continue

            audio = AudioFileClip(audio_path)
            duration = audio.duration
            text = section_data.get("text", "").strip()

            if not text:
                continue

            start = format_time(current_time)
            end = format_time(current_time + duration)

            lines.append(f"{counter}")
            lines.append(f"{start} --> {end}")
            lines.append(text)
            lines.append("")

            counter += 1
            current_time += duration

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return {
            "status": "success",
            "subtitle_path": output_path
        }
