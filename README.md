# Go Code Generator (GCG) 🛠️

An extensible AI Agent Orchestrator for generating Go CRUD code, Angular apps, GitHub automations, images, audio, video, subtitles, validations, and more — using local and cloud-based LLMs.

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

## 🧠 Supported Models

| Model | Use Case | Tags |
|:------|:---------|:-----|
| `ModelOllama` | Offline dev & chat | [Local], [LLM] |
| `ModelDeepSeekCoder67` | Advanced Go/Python/SQL code | [Local], [Code] |
| `ModelGpt4Turbo` | Structured workflows | [OpenAI] |
| `ModelGpt35Turbo` | Quick drafts | [OpenAI] |
| `ModelTTS1` | Cloud text-to-speech | [OpenAI], [Audio] |
| `ModelTTSCoqui` | Local TTS via Coqui | [Local], [Audio] |
| `ModelWhisper` | Speech-to-text | [OpenAI], [Audio] |
| `ModelDalle2` | Text-to-image | [OpenAI], [Image] |
| `ModelDalle3` | High-quality text-to-image | [OpenAI], [Image] |
| `ImageModelStableDiffusion` | Local/remote image generation | [Local], [Image] |
| `ModelGptImage1` | GPT-4 Vision for image analysis | [OpenAI], [Vision] |

✅ Browse, filter, and preview models via Streamlit UI

---

## 🤖 Supported Agents

### 🧠 Core
- `ChatAgent` — General chat, Q&A, prompt-based ideas
- `GoCRUDAgent` — Generate full Go model + API + handlers
- `AngularAppAgent` — Build basic Angular UIs

### 🎨 Image & Audio
- `Dalle3Agent`, `Dalle2Agent`
- `ImageAgent` — Unified image creation with any model
- `SegmentedImageAgent` — Per-section image rendering
- `AudioAgent` — TTS/STT handler (OpenAI + Coqui)
- `SegmentedAudioAgent` — Structured section narration
- `SegmentedSubtitleGeneratorAgent` — Auto-generate `.srt` files
- `SegmentedVideoAssemblerAgent` — Compose audio+image to video
- `ImageAnalysisAgent` — Analyze image using GPT-4 Vision

### ✅ Validators
- `ScriptStructureValidatorAgent` — Checks YAML structure
- `ScriptFeedbackValidatorAgent` — Gives recommendations + scores
- (Custom validators support `status/pass/fail`, conditions)

### 🛠️ Utilities
- `SaveToFileAgent`, `RequirementsExtractorAgent`
- GitHub automation agents (branch, commit, PR)
- Retrieval Augmented Generation (`RAG*` agents)

---

## 🎬 Segmented Video Workflow

Generate narrated videos step-by-step:

1. `ChatAgent` → generate script with `text` + `image_prompt`
2. `SegmentedAudioAgent` → create audio for each section
3. `SegmentedImageAgent` → generate scene visuals
4. `SegmentedSubtitleGeneratorAgent` → create `.srt` captions
5. `SegmentedVideoAssemblerAgent` → merge assets into `.mp4`

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

  - name: generate_image
    type: ai-image
    agent: ImageAgent
    model: ImageModelStableDiffusion
    input:
      prompt: "Thumbnail for: ${topic}"
      output_path: workspace/images/${name}.png
```

---

## 📊 Validators with Conditional Logic

```yaml
- name: validate_script
  type: validator
  agent: ScriptStructureValidatorAgent
  input:
    input_data: "{{ generate_script.result }}"
    expected_sections: ["intro", "background", "conclusion"]

- name: improve_script
  type: ai
  condition: "{{ validate_script.result.status == 'fail' }}"
  agent: ScriptFeedbackValidatorAgent
  model: ModelGpt35Turbo
  input:
    script: "{{ generate_script.result }}"
```

---

## 📦 Local Model Setup

### 🦙 Ollama
```bash
ollama pull llama3
ollama run llama3
```

### 🐸 Coqui TTS
```bash
pip install TTS
tts --model_name tts_models/en/ljspeech/tacotron2-DDC --download
```

### Sample Python
```python
from TTS.api import TTS
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
tts.tts_to_file("Hello world", file_path="output.wav")
```

---

## 🐳 Docker Support

```bash
docker build -t gcg-agent .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key gcg-agent
```

Streamlit UI:

```bash
docker run -p 8501:8501 -e OPENAI_API_KEY=your-key gcg-agent streamlit run ui.py
```

---

## 📂 Project Layout

| Folder | Purpose |
|--------|---------|
| `workflows/` | YAML workflow definitions |
| `agents/` | Modular AI agent logic |
| `models/` | Model integration classes |
| `schemas/` | JSON/YAML validation schemas |
| `utils/` | Common tools, printer, formatters |
| `api/` | FastAPI server |
| `run_cli.py` | CLI orchestrator |
| `ui.py` | Streamlit interface |

---

## ⚙️ Workflow Syntax

| Syntax | Example |
|--------|---------|
| `${var}` | `${topic}` |
| `{{ var }}` | `{{ name }}` |
| `step.result` | `generate_script.result` |
| `{{ step.result }}` | `{{ validate_script.result }}` |

---

## ✅ System Validation

```bash
python3 run_cli.py --validate
```

Or via Streamlit > Validation tab

---

## 🔀 Conditional Step Execution with `when`

Each workflow step can now include an optional `when` field to conditionally control whether it should run.

### ✅ Supported Formats

| Type      | Example                                       | Description                            |
|-----------|-----------------------------------------------|----------------------------------------|
| Literal   | `when: true`                                  | Always run                             |
| Expression| `when: "{{ validate_step.status == 'fail' }}"`| Evaluates based on previous results    |
| Variable  | `when: "{{ doit }}"`                          | Controlled by a value in `vars:`       |

### 📌 Example

```yaml
vars:
  doit: true

steps:
  - name: validate_step
    type: validator
    agent: ScriptStructureValidatorAgent
    input:
      input_data: "{{ script }}"
      expected_sections: ["intro", "body", "end"]

  - name: fix_script
    type: ai
    agent: ScriptFeedbackValidatorAgent
    model: ModelGpt35Turbo
    when: "{{ validate_step.status == 'fail' }}"
    input:
      script: "{{ script }}"

  - name: log_result
    type: utils
    agent: SaveToFileAgent
    when: "{{ doit }}"
    input:
      content: "{{ fix_script.result }}"
      file_path: ./logs/fix.txt


---

## 🗨️ Orchestrator Chat with Memory

Plan complex YAML workflows through an iterative chat interface — powered by the OrchestratorAgent.

### 🧠 Features

- Chat-like prompt entry with per-session memory
- Remembers previous instructions and improves outputs over time
- Select from multiple LLMs (GPT-4, Ollama, DeepSeek, etc.)
- Choose prompt templates (`default`, `data_only`, `spanish`)
- Preview, validate, and run generated workflows

### 🖥️ Streamlit UI

- Navigate to **Chat** page
- Enter a `Session ID` to start or continue a memory thread
- Submit instructions like:

```text
Create a workflow to clone https://github.com/user/repo.git
Then generate CRUD endpoints for Product
Add Angular frontend and Swagger docs

YAML is generated live and stored with history in workspace/memory_<session>.json


🧑‍💻 CLI Mode

```
python3 run_cli.py --orchestrator_chat \
  --session_id dev01 \
  --question "Create a CRUD workflow for Customer"
```

- Result is saved to workspace/memory_dev01.json

- Reuse the same session ID to refine, extend, or run the workflow

---

## 🌐 FastAPI API Server

Run your workflow as an API:

```bash
export GCG_API_KEY=your-key
python3 api/main.py
```

POST `/run-workflow`
```json
{
  "workflow_file": "examples/youtube/wf_segmented_01.yaml"
}
```

Headers:
```http
x-api-key: your-key
```

---

## 📜 License

MIT — Fork it, use it, build your own!

---

## 🚀 Final Notes

✅ Modular YAML agents  
✅ Multimodal pipelines (Text, Audio, Video)  
✅ Flexible CLI / API / UI orchestration  
✅ Works offline & online  
✅ Extendable with your own agents & models
