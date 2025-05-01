📄 models.md

# Supported Models

| Model                | Best Use                     | Tags                     |
|----------------------|------------------------------|--------------------------|
| ModelOllama          | Offline dev, small tasks     | [Local]                  |
| ModelDeepSeekCoder67 | Heavy coding tasks (Go, SQL) | [Local], [Code]          |
| ModelGpt4Turbo       | Structured planning, scripts | [OpenAI], [Advanced]     |
| ModelGpt35Turbo      | Fast drafts, chat, Q&A       | [OpenAI]                 |
| ModelDalle3          | Image generation             | [OpenAI], [Image]        |
| ModelTTS1            | Text-to-Speech               | [OpenAI], [Audio]        |
| ModelWhisper         | Speech-to-Text               | [OpenAI], [Audio]        |

## Extending Models

1. Add a new model class in `models/`
2. Register the model in `model_registry.py`
3. Include `description` and `tags` in your model's metadata

---

✅ New models are auto-discoverable in the UI and CLI.

