import argparse
import os, sys
from orchestrator_core import run_workflow
from config import __version__, __app_name__, __workflow_path__
from prompt_loader import PromptLoader
from agents.orchestratoragent import OrchestratorAgent
import validate
from memory_manager import load_memory, save_memory
from models.model_registry import MODEL_REGISTRY


def test_all_prompts():
    loader = PromptLoader()
    all_prompts = loader.list_prompts()

    dummy_data = {
        "model": "TestModel",
        "fields": "ID (int), Name (string), CreatedAt (timestamp)",
        "description": "Example description text"
    }

    print("\n🧪 Prompt Test Results:")
    for agent, templates in all_prompts.items():
        print(f"\n🔹 Agent: {agent}")
        for name in templates:
            try:
                template = loader.load_prompt(agent, name)
                rendered = template.format(**dummy_data)
                if "{" in rendered and "}" in rendered:
                    print(f"  [⚠️] {name}: Possibly unfilled placeholders")
                else:
                    print(f"  [✅] {name}: OK")
            except KeyError as e:
                print(f"  [❌] {name}: Missing placeholder → {e}")
            except Exception as e:
                print(f"  [💥] {name}: Unexpected error → {e}")
    print("")


def list_available_prompts():
    loader = PromptLoader()
    all_prompts = loader.list_prompts()

    print("\n📜 Available Prompts:")
    for agent, prompts in all_prompts.items():
        print(f"- {agent}")
        for p in prompts:
            print(f"  • {p}")
    print("")


def main():
    parser = argparse.ArgumentParser(description="Run an AI agent workflow.")
    parser.add_argument("--workflow", type=str, help="Path to the workflow file")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument("--prompt_list", action="store_true", help="List all available prompts and exit")
    parser.add_argument("--prompt_test", action="store_true", help="Test all prompt templates with dummy data")
    parser.add_argument("--validate", action="store_true", help="Validate agents, models, workflows")  # 🔥 NEW

    # 🧠 New chat arguments
    parser.add_argument("--chat", action="store_true", help="Run orchestrator with memory")
    parser.add_argument("--session_id", type=str, help="Session ID for memory")
    parser.add_argument("--question", type=str, help="Prompt/question to send to the orchestrator")
    parser.add_argument("--model", type=str, default="ModelGpt35Turbo", help="Model name to use")
    parser.add_argument("--template", type=str, default="default", help="Prompt template name")


    args = parser.parse_args()

    if args.chat:
        if not args.session_id or not args.question:
            raise ValueError("--session_id and --question are required for orchestrator_chat")

        memory = load_memory(args.session_id)
        prompt_loader = PromptLoader()
        prompt_template = prompt_loader.load_prompt("OrchestratorAgent", args.template)

        llm = MODEL_REGISTRY[args.model](temperature=0.3)
        agent = OrchestratorAgent(llm, prompt_template)

        result = agent.run(request=args.question, memory=memory)

        memory["history"].append({
            "request": args.question,
            "workflow": result.get("yaml", ""),
            "file": result.get("path")
        })
        memory["latest_workflow"] = result.get("path")

        save_memory(memory, args.session_id)
        print("✅ Workflow generated and memory updated.")
        print(f"📄 Saved to: {result.get('path')}")
        return

    if args.version:
        print(f"{__app_name__} version {__version__}")
        return

    if args.prompt_list:
        list_available_prompts()
        return 

    if args.prompt_test:
        test_all_prompts()
        return

    # ✅ Handle Validation Option
    if args.validate:
        validate.main()
        sys.exit(0)

    if not args.workflow:
        print("❌ Please provide a workflow file with --workflow <file>")
    else:
        workflow_path = os.path.join(__workflow_path__, args.workflow)
        run_workflow(workflow_path)


if __name__ == "__main__":
    main()
