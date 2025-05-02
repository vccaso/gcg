# Go Code Generator (GCG) 🛠️

An extensible AI Agent Orchestrator for generating Go CRUD code, Angular apps, GitHub automations, images, audio, video, and more — using local and remote LLMs!

Built with:

- 🧠 Python 3
- 🖥️ Streamlit (UI)
- 📜 YAML-based workflow definitions
- 🌐 OpenAI / Ollama / DeepSeek integrations
- 🐳 Docker optional support

---

# 📆 Requirements

- Python 3.8+
- Docker (optional)
- Access to LLMs (OpenAI API key or local Ollama models)

---

# 🔧 Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# OR
.venv\Scripts\activate      # Windows
```

### 3. Install Required Packages
```bash
pip install --no-cache-dir -r requirements.txt
```

---

# 🧠 Supported LLM Models

| Model | Best Use | Tags |
|:------|:---------|:-----|
| `ModelOllama` | Offline coding tasks | [Local] |
| `ModelDeepSeekCoder67` | Go/Python/SQL code | [Local], [Code] |
| `ModelGpt4Turbo` | Structured workflows | [OpenAI] |
| `ModelGpt35Turbo` | Fast, cheap drafts | [OpenAI] |
| `ModelDalle3` | Image generation | [OpenAI], [Image] |
| `ModelTTS1` | Text-to-Speech | [OpenAI], [Audio] |
| `ModelWhisper` | Speech-to-Text | [OpenAI], [Audio] |

✅ Model Registry available via UI!

---

# 🤖 Supported AI Agents

### 🧠 Core Agents
- `ChatAgent` — General chat/Q&A
- `GoCRUDAgent` — Full Go CRUD stack
- `AngularAppAgent` — Angular frontend builder

### 🎨 Visual & Audio Agents
- `Dalle3Agent` — Text-to-image
- `SegmentedImageAgent` — Multiple image prompts from structured script
- `AudioAgent` — TTS & STT
- `SegmentedAudioAgent` — Per-section audio files
- `SegmentedSubtitleGeneratorAgent` — Subtitle (SRT) from script & audio
- `SegmentedVideoAssemblerAgent` — Build video from segmented media

### 🗃️ RAG & Utility
- `RAGDatabaseBuilderAgent`, `RAGQueryAgent`, etc.
- `SaveToFileAgent`, `RequirementsExtractorAgent`, etc.

✅ Dynamic Agent Registry available via UI

---

# 🚀 Example Usage

### CLI Mode
```bash
python3 run_cli.py --workflow examples/youtube/wf_segmented_01.yaml
```

Other CLI Options:
```bash
python3 run_cli.py --prompt_list
python3 run_cli.py --prompt_test youtube
python3 run_cli.py --validate
```

### Streamlit UI
```bash
streamlit run ui.py
```
- Browse workflows
- Select models/agents
- Run & visualize outputs!

---

# 🎬 Segmented Video Generation

Structured YAML scripts now support `text` + `image_prompt` per section (intro, scene1, ...). Combine them into full narrated videos:

### Key Agents:
- `SegmentedAudioAgent`: generates per-section voice
- `SegmentedImageAgent`: creates image per scene
- `SegmentedSubtitleGeneratorAgent`: builds `.srt` file
- `SegmentedVideoAssemblerAgent`: merges all into final `.mp4`

---

# 🌐 OpenAI Setup

```bash
export OPENAI_API_KEY=your-key     # macOS/Linux
set OPENAI_API_KEY=your-key        # Windows
```

---

# 💻 Local Models (Ollama, DeepSeek)

Install Ollama: [https://ollama.com/download](https://ollama.com/download)

```bash
ollama pull llama3
ollama run llama3

To create a local TTS system using Ollama

Install Coqui TTS:
```
pip install TTS
```
Set Up the TTS Engine
For Coqui TTS, download a pre-trained model:

```
tts --list_models
tts --model_name tts_models/en/ljspeech/tacotron2-DDC --download
```

Integrate with Ollama
Use Python to connect Ollama's output to the TTS engine:
```
import ollama
from TTS.api import TTS

# Initialize Ollama
client = ollama.Client()
response = client.generate(prompt="Hello, how can I assist you today?")

# Initialize TTS
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
tts.tts_to_file(text=response['text'], file_path="output.wav")

```

Play the Generated Audio

Use a Python library like playsound or pydub to play the output.wav file:

```
from playsound import playsound
playsound("output.wav")
```


# Optional
export DEEPSEEK_URL=http://localhost:11434
```

---

# 📂 Project Structure

| Folder | Description |
|--------|-------------|
| `workflows/` | YAML workflow definitions |
| `agents/` | All agent classes |
| `models/` | Model integrations |
| `schemas/` | JSON schema validation |
| `utils/` | Utility functions |
| `api/` | FastAPI-based HTTP server |
| `run_cli.py` | CLI entry point |
| `ui.py` | Streamlit frontend |

---

# 🛠 Docker Support

```bash
docker build -t gcg-agent .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key gcg-agent
```

Or run Streamlit UI inside Docker:

```bash
docker run -p 8501:8501 -e OPENAI_API_KEY=your-key gcg-agent streamlit run ui.py
```

---

# 📄 Workflow Expression Support

| Pattern | Example | From |
|---------|---------|------|
| `${var}` | `${topic}` | from `vars:` |
| `step.result` | `step1.result` | from previous step |
| `{{ var }}` | `{{ filename }}` | Jinja |
| `{{ step.result }}` | `{{ generate_script.result }}` | Jinja |

---

# ✅ Validation

```bash
python3 run_cli.py --validate
```

Or from the Streamlit UI > Validation page.

---

# 🌍 FastAPI API

Run workflows via HTTP!

```bash
export GCG_API_KEY=secret-key
python3 api/main.py
```

POST `/run-workflow`:
```json
{
  "workflow_file": "examples/youtube/wf_segmented_01.yaml"
}
```

Headers:
```http
x-api-key: secret-key
```

---

# 🤝 License

MIT — Open to contribute & extend!

---

# 🌟 Final Words

✅ Compose powerful workflows  
✅ Scale AI pipelines easily  
✅ Orchestrate agents for real-world dev, content, and automation!
