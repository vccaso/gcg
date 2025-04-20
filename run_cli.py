import argparse
import os
from orchestrator_core import run_workflow
from config import __version__, __app_name__, __workflow_path__
from prompt_loader import PromptLoader


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



    args = parser.parse_args()

    if args.version:
        print(f"{__app_name__} version {__version__}")
        return

    if args.prompt_list:
        list_available_prompts()
        return 

    if args.prompt_test:
        test_all_prompts()
        return

    if not args.workflow:
        print("❌ Please provide a workflow file with --workflow <file>")
    else:
        workflow_path = os.path.join(__workflow_path__, args.workflow)
        run_workflow(workflow_path)


if __name__ == "__main__":
    main()
