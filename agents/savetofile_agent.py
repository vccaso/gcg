import os
import sys
from agents.base import BaseAgent
from utils.printer import Printer


class SaveToFileAgent(BaseAgent):
    def run(self, content, file_path: str, append: bool = True) -> str:
        mode = "a" if append else "w"
        try:
            with open(file_path, mode, encoding="utf-8") as f:
                if isinstance(content, list):
                    f.write("\n".join(content) + "\n")
                else:
                    f.write(str(content) + "\n")

            Printer.success(f"✅ Content saved to '{file_path}' ({'append' if append else 'overwrite'})")
            return f"Content saved to '{file_path}'"

        except Exception as e:
            Printer.error(f"❌ Failed to write to '{file_path}': {e}")
            return "[Error saving to file]"
