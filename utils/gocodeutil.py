import re

class GoCodeUtil:

    @staticmethod
    def extract_go_code_block(output: str) -> str:
        """
        Extracts only the content between the first ```go and ``` block.
        Ignores any extra content after the closing triple backticks.
        """
        match = re.search(r"```go\s+(.*?)```", output, re.DOTALL)
        if match:
            code_block = match.group(1).strip()
            code_block = code_block.replace("```","")
            return code_block
        return output.strip()
    

    @staticmethod
    def strip_markdown_formatting(text: str) -> str:
        if text.startswith("```go"):
            text = text.replace("```go", "", 1)
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
    