import os
import re
from models.modelbase import ModelBase
from utils.printer import Printer
from utils.gocodeutil import GoCodeUtil
from config import debug
import openai
import requests


class GoCRUDAgentOriginal:
    def __init__(self, llm: ModelBase, prompt_template: str):
        if not isinstance(llm, ModelBase):
            raise ValueError("LLM model must be an instance of ModelBase")
        self.llm = llm
        self.prompt_template = prompt_template

    def generate_prompt(self, **kwargs) -> str:
        """
        Fills in the prompt template using keyword arguments.
        Example:
            prompt_template = "Generate CRUD for model {model} with fields {fields}"
            kwargs = { "model": "Product", "fields": "ID, Name, Price" }
        """
        try:
            return self.prompt_template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing placeholder in template: {e}")

    def run(self, **kwargs) -> str:
        """
        Generates the final CRUD code from provided keyword arguments to fill the prompt.
        Returns clean Go code without markdown artifacts.
        """
        final_prompt = self.generate_prompt(**kwargs)
        crud_code = self.llm.get_response(final_prompt)

        # Strip code block formatting if present
        crud_code = GoCodeUtil.strip_markdown_formatting(crud_code)
        if debug:
            print(crud_code)
        return crud_code



class GoCRUDDataAgent:
    def __init__(self, llm: ModelBase, prompt_template: str):
        self.llm = llm
        self.prompt_template = prompt_template

    def generate_prompt(self, **kwargs) -> str:
        model_name = kwargs.get("model")
        if model_name:
            kwargs.setdefault("Model", model_name[0].upper() + model_name[1:])
            kwargs.setdefault("model_lowercase", model_name.lower())

        return self.prompt_template.format(**kwargs)

    def run(self, **kwargs):
        final_prompt = self.generate_prompt(**kwargs)
        llm_response = self.llm.get_response(final_prompt).strip()
        # Write files
        written_files = self.write_data_file(llm_response)
        return "\n".join(written_files)

    def write_data_file(self, go_code: str) -> list:
        parts = re.split(r"==== (.+?)\/n", go_code)
        written = []
        for i in range(1, len(parts), 2):
            path = parts[i].strip()
            code = parts[i + 1].strip()
            go_code = GoCodeUtil.extract_go_code_block(code)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(go_code + "\n")
            written.append(path)
        return written


class GoCRUDAgent:
    def __init__(self, llm: ModelBase, prompt_template: str):
        if not isinstance(llm, ModelBase):
            raise ValueError("LLM model must be an instance of ModelBase")
        self.llm = llm
        self.prompt_template = prompt_template

    def write_files_from_output(self, output: str) -> list:
        """
        Parses code output marked with:
        ==== ./some/path/to/file.go/n
        Writes or updates files:
        - Overwrites model/ and data/
        - Updates http/api/ and http/server.go if file exists
        Returns a list of written/updated file paths.
        """
        written_files = []
        parts = re.split(r"==== (.+?)\/n", output)

        for i in range(1, len(parts), 2):
            file_path = parts[i].strip()
            new_content = parts[i + 1].strip()

            go_code = GoCodeUtil.extract_go_code_block(new_content)
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Detect mode: overwrite or update
            if "http/api/" in file_path or file_path.endswith("server.go"):
                # Update logic: append to existing file
                if os.path.exists(file_path):
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write("\n\n// === AI-generated addition ===\n")
                        f.write(go_code + "\n")
                    action = "updated"
                else:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(go_code + "\n")
                    action = "created"
            else:
                # Default: overwrite
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content + "\n")
                action = "written"

            written_files.append(f"{file_path} ({action})")

        return written_files

    def generate_prompt(self, **kwargs) -> str:
        """
        Fills in the prompt template using keyword arguments.
        Example:
            prompt_template = "Generate CRUD for model {model} with fields {fields}"
            kwargs = { "model": "Product", "fields": "ID, Name, Price" }
        """
        try:
            return self.prompt_template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing placeholder in template: {e}")

    def run(self, **kwargs) -> str:
        """
        Generates CRUD Go code and updates files intelligently where needed.
        """

        local_repo_dir = kwargs.get("local_repo_dir", ".")

        # Load existing API file content if exists
        api_path = os.path.join(local_repo_dir, "http/api", f"{kwargs['model']}.go")
        if os.path.exists(api_path):
            with open(api_path, "r", encoding="utf-8") as f:
                kwargs["existing_api"] = f.read()
        else:
            kwargs["existing_api"] = ""

        # Load existing server.go if exists
        server_path = os.path.join(local_repo_dir, "http", "server.go")
        if os.path.exists(server_path):
            with open(server_path, "r", encoding="utf-8") as f:
                kwargs["existing_routes"] = f.read()
        else:
            kwargs["existing_routes"] = ""

        final_prompt = self.generate_prompt(**kwargs)
        crud_code = self.llm.get_response(final_prompt)
        crud_code = GoCodeUtil.strip_markdown_formatting(crud_code)

        written_files = self.write_files_from_output(crud_code)

        if debug:
            print(f"[📁] Files written:\n- " + "\n- ".join(written_files))

        return crud_code


class GoSwaggerAgent:
    def __init__(self, llm: ModelBase, prompt_template):
        if not isinstance(llm, ModelBase):
            raise ValueError("LLM model must be an instance of ModelBase")
        self.llm = llm
        self.prompt_template = prompt_template


    def get_go_files(self, local_repo_dir):
        """
        Walk through LOCAL_REPO_DIR and return a list of paths for .go files.
        """
        go_files = []
        for root, dirs, files in os.walk(local_repo_dir):
            for file in files:
                if file.endswith(".go"):
                    go_files.append(os.path.join(root, file))
        return go_files


    def run(self, local_repo_dir):

        go_files = self.get_go_files(local_repo_dir)
        if not go_files:
            print("No Go files found in the repository.")
        else:
            for file_path in go_files:
                print(f"Processing file: {file_path}")

                with open(file_path, 'r', encoding='utf-8') as f:
                    original_code = f.read()

                # prepare the promt
                final_prompt = self.prompt_template.format(original_code=original_code)
                # call the model
                response = self.llm.get_response(final_prompt)

                # Optionally remove markdown formatting.
                if response.startswith("```go"):
                    response = response.replace("```go", "").strip()
                if response.endswith("```"):
                    response = response[:-3].strip()

                # Write back the updated code.
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response)
                Printer.success(f"Processed and updated {file_path}")

class Dalle3Agent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def generate_image(self, prompt: str, image_path: str = None, size="1024x1024", quality="standard", style="vivid") -> dict:
        """
        Generates an image using DALL·E 3 and optionally saves it to disk.

        Parameters:
        - prompt: Image description
        - image_path: Local path to save the image (e.g., output/image.png)
        - size: Image size for DALL·E 3
        - quality: 'standard' or 'hd'
        - style: 'vivid' or 'natural'

        Returns:
        - A dictionary with image URL, saved path (if any), and revised prompt
        """
        try:
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size=size,
                quality=quality,
                style=style
            )
            image_data = response.data[0]
            image_url = image_data.url
            revised_prompt = getattr(image_data, "revised_prompt", prompt)

            result = {"url": image_url, "revised_prompt": revised_prompt}

            if image_path:
                self._download_image(image_url, image_path)
                result["saved_to"] = image_path

            return result

        except Exception as e:
            print(f"❌ Error generating or downloading image: {e}")
            return {"error": str(e)}

    def _download_image(self, url: str, path: str):
        """
        Downloads image from a URL and saves to local disk.
        """
        response = requests.get(url)
        response.raise_for_status()

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(response.content)
            
class Dalle2Agent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def generate_image(self, prompt: str, size="256x256") -> dict:
        """
        Generates an image using DALL·E 3 from the given prompt.

        Parameters:
        - prompt: Description of the image
        - size: Image size (256x256, 512x512 , or 1024x1024)

        Returns:
        - A dictionary with URL and optional metadata
        """
        try:
            response = openai.images.generate(
                model="dall-e-2",
                prompt=prompt,
                n=1,
                size=size,
                response_format="url"
            )
            image_data = response.data[0]
            return {
                "url": image_data.url,
                "revised_prompt": image_data.revised_prompt if hasattr(image_data, "revised_prompt") else prompt
            }
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return {"error": str(e)}

class AudioAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def text_to_speech(self, text: str, voice="alloy", model="tts-1", output_path="output/audio.wav") -> str:
        """
        Converts text to speech using OpenAI's TTS model and saves the audio file.
        """
        response = openai.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        response.stream_to_file(output_path)
        return output_path

    def speech_to_text(self, audio_file_path: str, model="whisper-1") -> str:
        """
        Transcribes an audio file to text using Whisper.
        """
        with open(audio_file_path, "rb") as f:
            transcript = openai.audio.transcriptions.create(
                model=model,
                file=f
            )
        return transcript.text

    def run(self, **kwargs):
        mode = kwargs.get("mode")

        if mode == "tts":
            return self.text_to_speech(
                text=kwargs["text"],
                voice=kwargs.get("voice", "alloy"),
                model=kwargs.get("model", "tts-1"),
                output_path=kwargs.get("output_path", "output/audio.wav")
            )

        elif mode == "stt":
            return self.speech_to_text(
                audio_file_path=kwargs["audio_file_path"],
                model=kwargs.get("model", "whisper-1")
            )

        else:
            raise ValueError("Invalid mode. Use 'tts' or 'stt'.")






