# Import all available model classes
from models.openai.model_gpt_35_turbo import ModelGpt35Turbo
from models.openai.model_gpt_4 import ModelGpt4
from models.openai.model_gpt_4_turbo import ModelGpt4Turbo
from models.local.model_llama3 import ModelOllama
from models.local.model_deepseek_coder import ModelDeepSeekCoder67
from models.openai.audio_model_openai import AudioModelOpenAI
from models.local.audio_model_coqui import AudioModelCoqui
from models.local.image_model_stable_diffusion import ImageModelStableDiffusion
from models.openai.model_gpt_image_1 import ModelGptImage1
from models.openai.model_gpt_dalle_3 import ModelDalle3
from models.openai.model_gpt_dalle_2 import ModelDalle2
from models.local.model_mistral import ModelOllamaMistral
from models.local.model_qwen3_8b import ModelQwen3_8b
from models.local.model_llama31_claude import ModelLlama31Claude

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
    "ImageModelStableDiffusion" : ImageModelStableDiffusion,
    "ModelGptImage1": ModelGptImage1,
    "ModelDalle3": ModelDalle3,
    "ModelDalle2": ModelDalle2,
    "ModelOllamaMistral": ModelOllamaMistral,
    "ModelQwen3_8b": ModelQwen3_8b,
    "ModelLlama31Claude": ModelLlama31Claude
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
    },
    "ImageModelStableDiffusion": {
        "short_description": "Generates images locally using Stable Diffusion.",
        "detailed_description": [
            "This model uses Stable Diffusion to generate high-quality images from text prompts.",
            "It can run locally or via a Hugging Face Inference Endpoint.",
            "Ideal for offline image generation, visual storytelling, or AI art creation."
        ],
        "tags": ["Local", "Image", "StableDiffusion"]
    },
    "ModelGptImage1": {
        "short_description": "GPT-4 Vision model that analyzes images alongside text prompts.",
        "detailed_description": [
            "Uses OpenAI's gpt-4-vision-preview endpoint to reason over both image and text input.",
            "Supports high-detail visual comprehension tasks like image description, OCR, layout understanding, and visual Q&A.",
            "Requires image input and a related prompt.",
            "Outputs natural language response based on combined input."
        ],
        "tags": ["OpenAI", "Image", "Multimodal", "Vision"]
    },
    "ModelDalle3": {
        "short_description": "OpenAI's DALL·E 3 model for high-quality image generation from text prompts.",
        "detailed_description": [
            "Generates detailed and coherent images based on textual descriptions.",
            "Improved understanding of nuanced prompts compared to previous versions.",
            "Integrated with ChatGPT for enhanced prompt generation and refinement.",
            "Includes safety features to prevent the creation of harmful or inappropriate content."
        ],
        "tags": ["OpenAI", "Image", "Text-to-Image", "DALL·E 3"]
    },
    "ModelDalle2": {
        "short_description": "OpenAI's DALL·E 2 model for basic image generation from text prompts.",
        "detailed_description": [
            "Generates simple, creative images based on text input.",
            "Faster and lighter than DALL·E 3, with support for standard sizes (256x256, 512x512, 1024x1024).",
            "Suitable for quick sketches, rough drafts, or experimental art.",
            "Lower fidelity and detail compared to DALL·E 3, but more efficient for some tasks."
        ],
        "tags": ["OpenAI", "Image", "Text-to-Image", "DALL·E 2"]
    },
    "ModelOllamaMistral": {
        "short_description": "Local Mistral model via Ollama",
        "detailed_description": (
            "Mistral is a dense 7B parameter language model optimized for reasoning and code generation. "
            "This model runs locally via Ollama, supports chat-style prompts with multi-turn memory, "
            "and provides strong performance in natural language understanding, making it ideal for dev tools, chatbots, and agents."
        ),
        "tags": ["Local", "LLM"]
    },
    "ModelQwen3_8b": {
        "short_description": "Qwen3 8B model via Ollama",
        "detailed_description": (
            "Qwen3 8B is part of Alibaba's third-generation language models. It features 8.19B dense parameters with "
            "an optimized architecture for general-purpose AI tasks, chat, and code reasoning. "
            "This model is served locally via Ollama with Q4_K_M quantization, supports Chinese and English fluency, and uses a dual-token format with stop control."
        ),
        "tags": ["Local", "LLM"]
    },
    "ModelLlama31Claude": {
        "short_description": "Llama 3.1 Claude-style via Ollama",
        "detailed_description": (
            "This model blends Meta's LLaMA 3.1 architecture with Claude Sonnet 3.5 system behavior. "
            "It has 8.03B parameters, runs via Ollama, and is configured with Claude-style role prompting. "
            "It's ideal for structured reasoning, document analysis, and assistant tasks that benefit from anthropic-style dialogue formatting and safety alignment."
        ),
        "tags": ["Local", "LLM"]
    }

}
