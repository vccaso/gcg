Go Code Generator (GCG) 🛠️
An extensible AI Agent Orchestrator for generating Go CRUD code, Angular apps, GitHub automations, images, audio, and more — using local and remote LLMs!

Built with:

🧠 Python 3

🖥️ Streamlit (for UI)

🔧 YAML-based workflow definitions

🌐 OpenAI / Ollama / DeepSeek integrations

📦 Requirements
Python 3.8+

Docker (optional, for containerized runs)

Access to LLMs (OpenAI API Key or Local Ollama Models)

🔧 Setup Instructions
1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/your-username/your-repo.git
cd your-repo
2. Create and Activate Virtual Environment
bash
Copy
Edit
python3 -m venv .venv
source .venv/bin/activate          # macOS/Linux
# OR
.venv\Scripts\activate             # Windows
3. Install Required Packages
bash
Copy
Edit
pip install -r requirements.txt
🧠 Supported LLM Models

Model	Best Use	Notes
ModelOllama	Offline dev, small tasks	Free, slower
ModelDeepSeekCoder67	Heavy coding (Go, Python, SQL)	Local coding genius
ModelGpt4Turbo	Structured code, planning	Best, more expensive
ModelGpt35Turbo	Fast drafts, simple tasks	Cheap, fast
ModelDalle3	Image generation	Text-to-image
ModelTTS1	Text-to-Speech	Create voice outputs
ModelWhisper	Speech-to-Text	Audio transcription
🧠 Supported AI Agents

Agent	Description
ChatAgent	General chat, Q&A, brainstorming
GoCRUDAgent	Full Go CRUD generator (model + API)
GoCRUDModelAgent	Only Go struct model generation
GoCRUDDataAgent	Only Go data access layer generation
GoSwaggerAgent	Swagger/OpenAPI doc generation
AngularAppAgent	Create Angular frontend code
Dalle3Agent	Generate images from text prompts
AudioAgent	Text-to-Speech and Speech-to-Text
SaveToFileAgent	Save content to a file
GitHubCreateBranchAgent	Create Git branches locally
GitHubCommitAgent	Make Git commits
GitHubCheckoutBranchAgent	Checkout Git branches
GitHubPRAgent	Create GitHub Pull Requests
GitHubCloneOrUpdateRepoAgent	Clone or update GitHub repos
🚀 Example Usage
Run from CLI:
bash
Copy
Edit
python3 run_cli.py --workflow workflows/wf_example.yaml
Use --workflow to point to any YAML workflow!

Run from Streamlit UI:
bash
Copy
Edit
streamlit run ui.py
Browse workflows, select, and launch them visually.

🌐 Using OpenAI Models
Make sure your API key is set:

bash
Copy
Edit
export OPENAI_API_KEY=your-api-key       # macOS/Linux
set OPENAI_API_KEY=your-api-key           # Windows
💻 Using Local Models (Ollama)
Install Ollama:
Download Ollama

Pull and Run Models:
bash
Copy
Edit
ollama pull llama3
ollama run llama3
List installed models:

bash
Copy
Edit
ollama list
🧠 Using DeepSeek Model Locally
Install DeepSeek via Ollama:
bash
Copy
Edit
ollama pull deepseek-coder:6.7b
Run DeepSeek Server:
bash
Copy
Edit
ollama run deepseek-coder
Available at:

bash
Copy
Edit
http://localhost:11434
Test DeepSeek with Curl:
bash
Copy
Edit
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "deepseek-coder",
  "prompt": "Explain Go channels."
}'
Set environment (optional):

bash
Copy
Edit
export DEEPSEEK_URL=http://localhost:11434
📂 Project Structure Overview

Folder	Purpose
workflows/	YAML workflow files
models/	LLM model wrappers (OpenAI, Ollama, etc.)
agents/	Custom agents for tasks (CRUD, GitHub, etc.)
http/	Generated Go API handlers and server setup
data/	Generated Go data access code
model/	Generated Go model structs
ui.py	Streamlit user interface
run_cli.py	CLI runner for workflows
🛠 Docker Support
Build Docker Image:
bash
Copy
Edit
docker build -t gcg-agent .
Run Container:
bash
Copy
Edit
docker run --rm \
  -e OPENAI_API_KEY=sk-... \
  -v $(pwd)/workflows:/app/workflows \
  gcg-agent
Mounts your workflows locally and passes API keys safely.

📜 Patterns Supported in Workflows

Pattern Type	Example	Resolved From
Variable	${my_var}	vars section
Step output	step_name.result	previous step
Jinja-style variable	{{ my_var }}	vars section
Jinja-style step output	{{ step_name.result }}	previous step
🤝 License
MIT License - Feel free to use and contribute!

🚀 Ready to Generate Code with AI!
Design YAML workflows

Run them locally or remotely

Generate Go apps, Angular apps, GitHub automation, images, audio, and more — all orchestrated by your AI agents!

🎯 Let's Code Smarter, Not Harder!