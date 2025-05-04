# Go Code Generator (GCG) 🛠️

An extensible AI Agent Orchestrator for generating Go CRUD code, Angular apps, GitHub automations, images, audio, video, subtitles, and more — using local and cloud-based LLMs.

---

## 🧰 Built With
- 🧠 Python 3
- 🖥️ Streamlit UI
- 📜 YAML-based workflow engine
- 🧩 Modular agent/model system
- 🌐 OpenAI, Ollama, DeepSeek, Coqui TTS
- 🐳 Optional Docker support

---

## 📆 Requirements

- Python 3.8+
- Pip + virtualenv
- Docker (optional)
- OpenAI or HuggingFace or Ollama access

---

## 🔧 Setup Instructions

```bash
git clone https://github.com/your-username/gcg.git
cd gcg
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install --no-cache-dir -r requirements.txt
```

---

## 🧠 Supported LLM Models

| Model | Use | Tags |
|:------|:----|:-----|
| `ModelOllama` | Offline dev & chat | [Local], [LLM] |
| `ModelDeepSeekCoder67` | Advanced coding (Go, Python) | [Local], [Code] |
| `ModelGpt4Turbo` | Structured workflows | [OpenAI] |
| `ModelGpt35Turbo` | Quick drafts | [OpenAI] |
| `ModelDalle3` | Text-to-image | [OpenAI], [Image] |
| `ModelTTS1` | Text-to-speech | [OpenAI], [Audio] |
| `ModelWhisper` | Speech-to-text | [OpenAI], [Audio] |
| `ModelTTSCoqui` | Offline text-to-speech (Coqui TTS) | [Local], [Audio] |
| `ImageModelStableDiffusion` | Local/remote image generation | [Local], [Image]

✅ Browse and filter models via Streamlit UI

---

## 🤖 Supported AI Agents

### 🧠 Core
- `ChatAgent` — General chat / idea generation
- `GoCRUDAgent` — Full Go CRUD generation
- `AngularAppAgent` — Angular frontend builder

### 🎨 Image & Audio
- `Dalle3Agent` — Generate image via DALL·E
- `ImageAgent` — Unified image agent w/ pluggable models
- `SegmentedImageAgent` — Image per scene/section
- `AudioAgent` — TTS/STT engine
- `SegmentedAudioAgent` — Per-section speech audio
- `SegmentedSubtitleGeneratorAgent` — Builds subtitles from TTS
- `SegmentedVideoAssemblerAgent` — Final video creator from image + audio

### ✅ Validators
- `ScriptStructureValidatorAgent` — Checks script sections
- `ScriptFeedbackValidatorAgent` — Scores script and suggests improved prompt

### 🛠️ Utility
- `SaveToFileAgent`, `RequirementsExtractorAgent`
- `GitHub*` agents (branch, commit, PR)
- `RAG*` agents for retrieval pipelines

✅ Filter & explore agents in Streamlit UI

---

## 🧪 Sample Workflow

```yaml
vars:
  topic: "How to prioritize tasks effectively"
  name: "productivity"

steps:
  - name: generate_script
    type: ai
    agent: ChatAgent
    model: ModelGpt35Turbo
    input:
      question: ${topic}

  - name: generate_audio
    type: ai-audio
    agent: AudioAgent
    model: ModelTTS1
    input:
      mode: tts
      text: "{{ generate_script.result }}"
      output_path: workspace/audio/${name}.wav
      factor: 1.4

  - name: generate_thumbnail
    type: ai-image
    agent: ImageAgent
    model: ImageModelStableDiffusion
    input:
      prompt: "Thumbnail for: ${topic}"
      output_path: workspace/images/${name}.png
```

---

## 🎬 Segmented Video Assembly

Compose narrated videos using multiple agents:

1. `ChatAgent` + YouTube template (text/image_prompt)
2. `SegmentedAudioAgent`
3. `SegmentedImageAgent`
4. `SegmentedSubtitleGeneratorAgent`
5. `SegmentedVideoAssemblerAgent`

---

## 🌐 OpenAI Configuration

```bash
export OPENAI_API_KEY=your-key
```

---

## 💻 Local Model Support

### 🦙 Ollama (for local LLMs)
```bash
ollama pull llama3
ollama run llama3
```

### 🐸 Coqui TTS (local TTS)
```bash
pip install TTS
tts --model_name tts_models/en/ljspeech/tacotron2-DDC --download
```

### Sample Python Usage
```python
from TTS.api import TTS
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
tts.tts_to_file("Hello world", file_path="output.wav")
```

---

## 📂 Project Layout

| Folder | Purpose |
|--------|---------|
| `workflows/` | YAML workflow definitions |
| `agents/` | Task-specific agents |
| `models/` | Audio, image, LLM models |
| `schemas/` | JSON validation schemas |
| `utils/` | YAML, JSON, printer helpers |
| `api/` | FastAPI server |
| `ui.py` | Streamlit UI |
| `run_cli.py` | CLI runner |

---

## 🐳 Docker Support

```bash
docker build -t gcg-agent .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key gcg-agent
```

Or for UI:

```bash
docker run -p 8501:8501 -e OPENAI_API_KEY=your-key gcg-agent streamlit run ui.py
```

---

## 🧪 Workflow DSL Support

| Pattern | Example | From |
|---------|---------|------|
| `${var}` | `${topic}` | `vars:` |
| `step.result` | `step1.result` | Previous step |
| `{{ var }}` | `{{ filename }}` | Jinja |
| `{{ step.result }}` | `{{ generate_script.result }}` | Jinja |

---

## ✅ Validation

```bash
python3 run_cli.py --validate
```

Or via Streamlit > Validation tab

---

## 🌍 API Server (FastAPI)

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

Header:
```http
x-api-key: secret-key
```

---

## 📜 License

MIT — Fork, contribute, and scale it your way!

---

## 💡 Final Words

✅ Design agent workflows  
✅ Run offline or cloud LLMs  
✅ Generate code, media, and content pipelines  
✅ Modular, extensible, and production-ready
