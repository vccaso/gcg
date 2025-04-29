# Go Code Generator (GCG) 🛠️

An extensible AI Agent Orchestrator for generating Go CRUD code, Angular apps, GitHub automations, images, audio, and more — using local and remote LLMs!

Built with:

- 🧠 Python 3
- 🖥️ Streamlit (UI)
- 🔧 YAML-based workflow definitions
- 🌐 OpenAI / Ollama / DeepSeek integrations
- 🛠️ Docker optional support

---

# 📆 Requirements

- Python 3.8+
- Docker (optional, for containerized runs)
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
pip install -r requirements.txt
```

``` windows
pip install --no-cache-dir -r requirements.txt
```

---

# 🧠 Supported LLM Models

| Model | Best Use | Notes | Tags |
|:-----|:---------|:------|:-----|
| ModelOllama | Offline dev, small tasks | Free, slower | [Local] |
| ModelDeepSeekCoder67 | Heavy coding (Go, Python, SQL) | Local coding genius | [Local], [Code] |
| ModelGpt4Turbo | Structured code, planning | Best, more expensive | [OpenAI] |
| ModelGpt35Turbo | Fast drafts, simple tasks | Cheap, fast | [OpenAI] |
| ModelDalle3 | Image generation | Text-to-image | [OpenAI], [Image] |
| ModelTTS1 | Text-to-Speech | Voice outputs | [OpenAI], [Audio] |
| ModelWhisper | Speech-to-Text | Audio transcription | [OpenAI], [Audio] |

✅ Dynamic Model Catalog available via UI filtering!

---

# 🤖 Supported AI Agents

| Agent | Description | Tags |
|:-----|:-------------|:-----|
| ChatAgent | General chat, Q&A, brainstorming | [AI] |
| GoCRUDAgent | Full Go CRUD generator (Model + API) | [AI], [Go] |
| GoCRUDModelAgent | Only Go struct model generation | [AI], [Go] |
| GoCRUDDataAgent | Only Go data access layer generation | [AI], [Go] |
| GoSwaggerAgent | Swagger/OpenAPI doc generation | [AI], [Go], [Swagger] |
| AngularAppAgent | Create Angular frontend code | [AI], [Frontend] |
| Dalle3Agent | Generate images from text prompts | [AI], [Image] |
| AudioAgent | Text-to-Speech and Speech-to-Text | [AI], [Audio] |
| SaveToFileAgent | Save content to a file | [Utility] |
| GitHubCreateBranchAgent | Create Git branches locally | [GitHub] |
| GitHubCommitAgent | Make Git commits | [GitHub] |
| GitHubCheckoutBranchAgent | Checkout Git branches | [GitHub] |
| GitHubPRAgent | Create GitHub Pull Requests | [GitHub] |
| GitHubCloneOrUpdateRepoAgent | Clone or update GitHub repos | [GitHub] |
| RequirementsExtractorAgent | Extract Python project dependencies | [Utility], [Python] |
| RAGDatabaseBuilderAgent | Build RAG vector database | [RAG], [Database] |
| RAGQueryAgent | Query a RAG vector database | [RAG], [Retrieval] |
| RAGAttachAgent | Attach docs to RAG database | [RAG], [Database] |
| RAGDatabaseUpdaterAgent | Update RAG embeddings | [RAG], [Database] |

✅ Dynamic Agent Catalog available via UI!

---

# 🚀 Example Usage

### Run from CLI:
```bash
python3 run_cli.py --workflow workflows/wf_example.yaml
```

Other CLI Options:
```bash
python3 run_cli.py --prompt_list       # List available prompt templates
python3 run_cli.py --prompt_test <name> # Test a prompt template
python3 run_cli.py --validate           # Validate all models, agents, and workflows ✅
```

### Run from Streamlit UI:
```bash
streamlit run ui.py
```
- Select **Workflows**
- Browse **Models** and **Agents** by **Tags**
- Run with full visibility and logs!

---

# 🌐 Using OpenAI Models

Make sure your API key is set:

```bash
export OPENAI_API_KEY=your-api-key       # macOS/Linux
set OPENAI_API_KEY=your-api-key           # Windows
```

---

# 💻 Using Local Models (Ollama)

Install Ollama:
- [Download Ollama](https://ollama.com/download)

Pull and Run Models:
```bash
ollama pull llama3
ollama run llama3
```

List installed models:
```bash
ollama list
```

---

# 🧠 Using DeepSeek Model Locally

Pull DeepSeek via Ollama:
```bash
ollama pull deepseek-coder:6.7b
```

Run DeepSeek Server:
```bash
ollama run deepseek-coder
```

Test DeepSeek with curl:
```bash
curl -X POST http://localhost:11434/api/generate -d '{"model":"deepseek-coder","prompt":"Explain Go channels."}'
```

Set Environment (Optional):
```bash
export DEEPSEEK_URL=http://localhost:11434
```

---

# 📂 Project Structure Overview

| Folder | Purpose |
|:-------|:--------|
| workflows/ | YAML workflow files |
| models/ | LLM model wrappers (OpenAI, Ollama, etc.) |
| agents/ | Custom task-specific agents |
| http/ | Generated Go HTTP server code |
| data/ | Generated Go data access layer |
| model/ | Generated Go model structs |
| ui.py | Streamlit UI application |
| run_cli.py | Command-line interface |
| validate.py | System validation tool |

---

# 🛠 Docker Support

## Build the Docker image
```
docker build -t gcg-agent .
```

## Run FastAPI Server
```
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-real-openai-key \
  -e GCG_API_KEY=your-real-api-key \
  gcg-agent
```
Your API is now available at http://localhost:8000

## (Optional) Run Streamlit UI

If you want to run the UI instead inside the container, you can override the CMD like this:
```
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your-real-openai-key \
  gcg-agent streamlit run ui.py
```
Streamlit UI available at http://localhost:8501


✅ Mounts local workflows
✅ Passes API keys safely

---

# 📄 Patterns Supported in Workflows

| Pattern Type | Example | Resolved From |
|:-------------|:--------|:--------------|
| Variable | `${my_var}` | `vars:` section |
| Step Output | `step_name.result` | previous step output |
| Jinja-style Variable | `{{ my_var }}` | `vars:` section |
| Jinja-style Step Output | `{{ step_name.result }}` | previous step output |

---

# ✅ System Validation

You can now validate your system before scaling up!

Validate Agents, Models, and Workflows easily:

```bash
python3 run_cli.py --validate
```

or from **Streamlit UI** (Validation Page).

---

# 🤝 License

MIT License — Feel free to use, fork, and contribute!

---

# 🌟 Final Words

✅ Design YAML Workflows
✅ Orchestrate AI Agents easily
✅ Scale to hundreds of tasks: Go Apps, Angular Apps, GitHub Automations, RAG Systems, and more!

---

# 📊 GCG API (FastAPI)

## Overview
You can run any YAML-based workflow via an HTTP API using FastAPI. This enables GCG to be used from external tools, UI clients, or integrations.

## Requirements
- FastAPI
- Uvicorn
- (Reuses existing `run_workflow()` from orchestrator_core)

### Install FastAPI and Uvicorn:
```bash
pip install fastapi uvicorn
```

## Running the API Server
```bash
export GCG_API_KEY=your-secure-key
python3 api/main.py
```

Server will be available at:
```
http://localhost:8000
```

## Endpoint: Run Workflow
**POST /run-workflow**

### Authentication Required
Header:
```http
x-api-key: your-secure-key
```

### Request Body (JSON)
```json
{
  "workflow_file": "wf_example.yaml"
}
```

### Response
```json
{
  "status": "success",
  "result": {
    "step_name": "...output..."
  }
}
```

## Example with Curl
```bash
curl -X POST http://localhost:8000/run-workflow \
  -H "Content-Type: application/json" \
  -H "x-api-key: 1234567890" \
  -d '{"workflow_file": "examples/content/wf_content.yaml"}'
```

## Deployment Options
- Local (for dev)
- Docker container (to deploy to cloud)
- Behind Nginx or API Gateway (optional extra auth)

## Roadmap
- [x] API key protection
- [ ] Run dynamic workflow from JSON
- [ ] Async background execution
- [ ] Job queue support (Celery/RQ)
