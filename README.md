# Go Code Generator  (GCG)


– To run this script you must install the required Python packages:
pip install GitPython openai requests



python3 main.py --profile avila-easychat-goals --promt inline-comments

python3 -m venv .venv
. venv/bin/activate
pip install -r requirements.txt





# 🤖 Local + Remote LLM Chat Engine

This project includes a modular LLM integration using:

- 🌐 OpenAI GPT-3.5-Turbo (via API)
- 💻 Ollama (run local models like LLaMA3, Mistral, etc.)

You can switch between providers by instantiating either `ModelGpt35Turbo` or `ModelOllama`, both implementing the same interface.

---

## 📦 Requirements

- Python 3.8+
- Virtual environment (recommended)

---

## 🔧 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo


#  Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# OR
venv\Scripts\activate           # Windows


# . Install dependencies
pip install -r requirements.txt

# Set OpenAI API Key (if using OpenAI GPT)
export OPENAI_API_KEY=your-api-key   # macOS/Linux
# OR
set OPENAI_API_KEY=your-api-key      # Windows

# Using Ollama (Local LLMs)

## Install Ollama
Download from: https://ollama.com/download
Then install a model, for example:

ollama pull llama3


## Make sure Ollama is running
Start Ollama in the background if it’s not already running:

```ollama run llama3```
ollama run llama3.2

You can replace llama3 with any local model like mistral, codellama, etc.

## 🚀 Example Usage
# Use OpenAI
```
from models.model_gpt35 import ModelGpt35Turbo
model = ModelGpt35Turbo()
print(model.get_response("Explain recursion."))

# Use Ollama

from models.model_ollama import ModelOllama
model = ModelOllama("llama3")
print(model.get_response("What is a hash map?"))
```


## List all downloaded models
ollama list

## List currently running models
ps aux | grep ollama


##  Start a model manually
ollama run llama3

## Remove a downloaded model
ollama rm llama3


## Pull a new model
ollama pull llama3
ollama pull mistral
ollama pull codellama

## You can browse available models here: https://ollama.com/library


🛠 Optional

Add .env support using python-dotenv if you want to keep secrets out of your shell
Add streamlit if you're building a UI

🤝 License

---








# 🤖 AI Agent Orchestrator

An extensible, YAML-driven AI Agent Orchestrator built with Python. This tool allows you to define and run custom workflows using specialized AI agents — perfect for tasks like code generation, GitHub automation, and more.

## ✨ Features

- ⚙️ YAML-based workflow definitions
- 🧠 Pluggable Python AI agents
- 🖥️ Streamlit-based UI to visualize and run workflows
- 💻 Command-line support for automation and CI/CD
- 🔄 Reusable step results across agents
- ✅ Easy-to-extend agent system

---

## 📁 Project Structure

✅ Supported Patterns

Pattern Type	Example	Resolved From
Variable	${my_var}	variables dict
Step result	step_name.result	context (workflow results)
Jinja-style variable	{{ my_var }}	variables
Jinja-style step result	{{ step_name.result }}	context
Mixed literals	Start of prompt: {{ step.result }}	Interpolated
