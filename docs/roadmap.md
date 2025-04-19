🗺️ OrishAI Roadmap


# 🗺️ OrishAI Project Roadmap

This roadmap outlines the planned development phases for OrishAI — a modular AI agent orchestration framework with support for workflows, RAG, local and cloud LLMs, and developer automation.

---

## ✅ MVP (Complete)

**Goal:** Establish a working orchestration engine with YAML workflow support, local agents, CLI and UI.

- [x] Agent base class and loader system
- [x] Workflow engine with `vars`, `steps`, and `${}` substitution
- [x] Streamlit and CLI interfaces
- [x] Support for:
  - `RAGDatabaseBuilderAgent`
  - `RAGQueryAgent`
  - `SaveToFileAgent`
  - `RequirementsExtractorAgent`
  - `GitHubCloneOrUpdateRepoAgent`
  - `GitHubCheckoutBranchAgent`

---

## 🔜 Phase 1: Workflow Usability & Developer Experience

**Goal:** Improve UX for authoring, debugging, and running workflows.

- [ ] Step-level error handling (don't crash on failure)
- [ ] Debug mode: print step output and variables
- [ ] Dry-run mode for YAML validation
- [ ] Auto-generate agent docs from Python classes
- [ ] Streamlit visualizer for workflow steps and dependencies
- [ ] Live registry of available agents + input schema

**⏱ ETA:** 2–3 weeks  
**📦 Priority:** ⭐⭐⭐⭐

---

## 🔜 Phase 2: RAG + AI Enhancements

**Goal:** Enhance retrieval quality, agent intelligence, and prompt flexibility.

- [ ] Document chunking with metadata (file, chunk ID)
- [ ] Similarity filtering by distance score
- [ ] Prompt templating using Jinja2 + `vars`
- [ ] Memory-enabled chat agents
- [ ] Model evaluation agent (`EvalAgent`) for comparing LLMs
- [ ] Token/cost usage tracking per step
- [ ] Tool-calling inside agents (e.g. one agent invoking others)

**⏱ ETA:** 3–4 weeks  
**📦 Priority:** ⭐⭐

---

## 🔜 Phase 3: Collaboration + Integration

**Goal:** Enable external triggers, integration with teams and cloud tools.

- [ ] REST API (`POST /run-workflow`, `GET /status`)
- [ ] Scheduled workflows (cron or periodic trigger)
- [ ] Slack / Discord / Email notification agents
- [ ] Integrations: Google Drive, Notion, GitHub PRs
- [ ] HTML / Markdown report generator agent
- [ ] Workflow export/import in JSON format

**⏱ ETA:** 4–5 weeks  
**📦 Priority:** ⭐⭐

---

## 🧪 Phase 4: Plugin Ecosystem / Marketplace

**Goal:** Let developers extend the framework with shareable agents and plugins.

- [ ] Plugin loader (pip-installable agents or zipped modules)
- [ ] Agent marketplace with rating/sharing system
- [ ] Custom visual UIs per step (in Streamlit)
- [ ] Agent test runner for mocks, inputs/outputs

**⏱ ETA:** 6–8 weeks  
**📦 Priority:** ⭐ (advanced/optional)

---

## 🧩 Bonus Features (Drop-in Ready)

- [ ] `when:` conditional logic per step
- [ ] `foreach:` support for looping over lists
- [ ] `output_format:` switch for JSON/text/markdown
- [ ] `save_logs: true` flag to persist logs per run

---

> This roadmap will evolve based on feedback, usage, and emerging AI capabilities. Community contributions are welcome!










Phase	Focus	Features	Priority
✅ MVP	Core orchestration engine	YAML workflows, Streamlit UI, CLI, agent runner, RAG, file I/O, LLM chat	✅ Complete
🔜 Phase 1: Workflow Usability & Developer Experience	Make authoring and debugging workflows smooth	⭐ High	
🔜 Phase 2: RAG + AI Enhancements	Smarter agents and memory	⭐⭐ Medium	
🔜 Phase 3: Collaboration + Cloud	Trigger + share + integrate	⭐ Medium	
🧪 Phase 4: Marketplace + Plugin Ecosystem	Extend + monetize	⭐⭐ Optional/Advanced	
✅ MVP (Complete)
Goal: Build a working orchestration framework

 Agent base class + agent runner

 Workflow YAML with vars, steps, ${} substitution

 CLI + Streamlit UI

 RAGDatabaseBuilderAgent, RAGQueryAgent, SaveToFileAgent, etc.

🔜 Phase 1: Workflow Usability & Developer Experience
🎯 Goal: Make it easy to author, test, and understand workflows

🔹 Features:
 content_from + step referencing

 ✅ Error handling per step: show failures in UI without crashing

 ✅ Dry-run mode: validate YAML without executing

 ✅ Debug mode: log variables, step outputs, errors

 ✅ Agent doc auto-generation from agents/*.py (AgentSpecAgent)

 ✅ Streamlit Workflow Visualizer: show steps, vars, and links

 ✅ Live agent registry: list available agents and their expected inputs

🕐 Estimated Time: 2–3 weeks
📦 Priority: ⭐⭐⭐⭐

🔜 Phase 2: RAG + AI Enhancements
🎯 Goal: Make agents smarter and enable powerful LLM workflows

🔹 Features:
 🧠 Chunked RAG ingestion with metadata

 🧠 RAG filtering by similarity score

 🧠 Prompt templates using Jinja2

 💬 ChatAgent with memory across sessions

 🧪 EvalAgent to compare model outputs (OpenAI vs Ollama)

 💰 Cost tracker (token usage / $ spent estimate)

 🧠 Tool-calling or agent-calling inside agents

🕐 Estimated Time: 3–4 weeks
📦 Priority: ⭐⭐

🔜 Phase 3: Collaboration + Integration
🎯 Goal: Trigger workflows from external tools and share results

🔹 Features:
 🌐 REST API: POST /run-workflow, GET /status

 ⏱️ Scheduled workflows (cron or interval)

 📤 Slack/Discord agents

 ☁️ Notion / Google Drive / GitHub integration

 🌍 Export workflows as JSON for dashboard or frontend apps

 📜 Markdown/HTML report generator agent

🕐 Estimated Time: 4–5 weeks
📦 Priority: ⭐⭐

🧪 Phase 4: Plugin Ecosystem / Marketplace
🎯 Goal: Let other devs build & share custom agents/workflows

🔹 Features:
 🔌 Plugin loader system (agents installed via pip or zip)

 🏪 Agent store / marketplace

 🧰 Custom step UIs (forms or visual config) in Streamlit

 🧪 Agent testing suite (mocking inputs & expected outputs)

🕐 Estimated Time: 6–8 weeks
📦 Priority: ⭐ (optional, good for scale)

🧩 Bonus Micro-Features (Drop-in ready)
 when: condition per step (boolean expression support)

 foreach: loop over lists

 output_format: json|text|md

 save_logs: true to auto-append logs to a folder

✅ Delivery Format Suggestion
Use GitHub Projects or Notion to track phases/tasks

Add a roadmap.md or visual timeline to your repo

Tag agent folders with phase-1, phase-2, etc. for clarity