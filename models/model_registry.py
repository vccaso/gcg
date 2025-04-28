# Import all available model classes
from models.openai.model_gpt_35_turbo import ModelGpt35Turbo
from models.openai.model_gpt_4 import ModelGpt4
from models.openai.model_gpt_4_turbo import ModelGpt4Turbo
from models.local.model_llama3 import ModelOllama
from models.local.model_deepseek_coder import ModelDeepSeekCoder67

# Optional: if you expect to add more local models later

# ✅ Central registry mapping model names to classes
MODEL_REGISTRY = {
    "ModelGpt35Turbo": ModelGpt35Turbo,
    "ModelGpt4Turbo": ModelGpt4Turbo,
    "ModelGpt4": ModelGpt4,
    # "ModelDalle3": ModelDalle3,
    # "ModelTTS1": ModelTTS1,
    # "ModelWhisper": ModelWhisper,
    "ModelOllama": ModelOllama,
    "ModelDeepSeekCoder67": ModelDeepSeekCoder67,
}

# ✅ Model catalog for UI display
MODEL_CATALOG = {
    "ModelGpt35Turbo": {
        "description": "Fast, cost-efficient model ideal for lightweight code tasks and quick drafts. (OpenAI)",
    },
    "ModelGpt4Turbo": {
        "description": "Powerful model best for structured code generation, logic-heavy workflows, and complex planning. (OpenAI)",
    },
    # "ModelDalle3": {
    #     "description": "Advanced model for generating high-quality images from text prompts. (OpenAI)",
    # },
    # "ModelTTS1": {
    #     "description": "Text-to-speech model for converting text into audio output. (OpenAI)",
    # },
    # "ModelWhisper": {
    #     "description": "Automatic speech recognition (ASR) model for transcribing audio to text. (OpenAI)",
    # },
    "ModelOllama": {
        "description": "Local model running via Ollama. Free and offline but slower compared to cloud models.",
    },
    "ModelDeepSeekCoder67": {
        "description": "Specialized coding model trained on 2 trillion tokens for heavy coding tasks (Go, Python, SQL). (Local via Ollama)",
    },
}