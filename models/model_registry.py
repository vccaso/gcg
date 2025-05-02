# Import all available model classes
from models.openai.model_gpt_35_turbo import ModelGpt35Turbo
from models.openai.model_gpt_4 import ModelGpt4
from models.openai.model_gpt_4_turbo import ModelGpt4Turbo
from models.local.model_llama3 import ModelOllama
from models.local.model_deepseek_coder import ModelDeepSeekCoder67
from models.openai.audio_model_openai import AudioModelOpenAI
from models.local.audio_model_coqui import AudioModelCoqui

# Optional: if you expect to add more local models later

# ✅ Central registry mapping model names to classes
MODEL_REGISTRY = {
    "ModelGpt35Turbo": ModelGpt35Turbo,
    "ModelGpt4Turbo": ModelGpt4Turbo,
    "ModelGpt4": ModelGpt4,
    "ModelOllama": ModelOllama,
    "ModelDeepSeekCoder67": ModelDeepSeekCoder67,
    "AudioModelOpenAI": AudioModelOpenAI,
    "AudioModelCoqui": AudioModelCoqui,
}

# ✅ Model catalog for UI display
MODEL_CATALOG = {
    "ModelOllama": {
        "short_description": "Local LLM running offline (free but slower).",
        "detailed_description": [
            "Local model running on your machine.",
            "Free to use but slower than cloud models.",
            "Good for basic chat, small tasks, and offline use."
        ],
        "tags": ["Local", "LLM"]
    },
    "ModelDeepSeekCoder67": {
        "short_description": "Specialized local coding model for Go, Python, JavaScript, and SQL.",
        "detailed_description": [
            "Specialized coding model trained on 2 trillion code + natural language tokens.",
            "Excels at generating Go, Python, JavaScript, SQL, and complex algorithms.",
            "Best choice for large, accurate code generation tasks."
        ],
        "tags": ["Local", "Coding", "LLM"]
    },
    "ModelGpt4Turbo": {
        "short_description": "OpenAI's most powerful model for complex tasks and structured code.",
        "detailed_description": [
            "Most powerful general model available.",
            "Best for structured code generation, logic-heavy workflows, and complex planning.",
            "Highly reliable but higher API cost."
        ],
        "tags": ["OpenAI", "LLM"]
    },
    "ModelGpt35Turbo": {
        "short_description": "Fast, cheaper OpenAI model ideal for lightweight coding and brainstorming.",
        "detailed_description": [
            "Fast and cost-efficient.",
            "Good for lightweight code tasks, brainstorming, chatbots, or simple CRUD generation.",
            "Slightly less accurate on complex tasks."
        ],
        "tags": ["OpenAI", "LLM"]
    },
    "ModelDalle3": {
        "short_description": "Generates high-quality images from text prompts (DALL·E 3).",
        "detailed_description": [
            "Advanced model for generating high-quality images from text prompts.",
            "Ideal for creating marketing banners, UI designs, visual content."
        ],
        "tags": ["OpenAI", "Image"]
    },
    "ModelTTS1": {
        "short_description": "Text-to-speech (TTS) model converting text into spoken audio.",
        "detailed_description": [
            "Text-to-speech model.",
            "Converts text into high-fidelity spoken audio (multiple voices available).",
            "Use for welcome messages, voice notifications, or audio content generation."
        ],
        "tags": ["OpenAI", "Audio", "TTS"]
    },
    "ModelWhisper": {
        "short_description": "Speech-to-text (ASR) model transcribing audio recordings.",
        "detailed_description": [
            "Automatic speech recognition (ASR) model.",
            "Transcribes audio recordings (.mp3, .wav) into text.",
            "Best for meeting notes, interviews, podcasts, or audio summarization."
        ],
        "tags": ["OpenAI", "Audio", "STT"]
    },
    "AudioModelOpenAI": {
        "short_description": "OpenAI TTS model (e.g. alloy, tts-1).",
        "detailed_description": [
            "Cloud-based text-to-speech using OpenAI's TTS API.",
            "Supports multiple voices and high quality audio.",
            "Requires OpenAI API key and internet connection."
        ],
        "tags": ["Audio", "TTS", "OpenAI"]
    },
    "AudioModelCoqui": {
        "short_description": "Offline TTS using Coqui (TTS CLI).",
        "detailed_description": [
            "Runs text-to-speech locally using the Coqui TTS engine.",
            "Supports multiple models and speaker configurations.",
            "No internet required, suitable for local/edge deployment."
        ],
        "tags": ["Audio", "TTS", "Local", "Coqui"]
    }
}
