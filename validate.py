# validate.py

import os
import yaml
from colorama import init, Fore, Style

# Init colorama
init(autoreset=True)

# Imports
from models.model_registry import MODEL_CATALOG
from agents.agent_registry import AGENT_CATALOG
from config import __workflow_path__

def validate_agents():
    errors = []
    for agent_name, agent_info in AGENT_CATALOG.items():
        if "short_description" not in agent_info:
            errors.append(f"Agent '{agent_name}' missing short_description.")
        if "tags" not in agent_info or not agent_info["tags"]:
            errors.append(f"Agent '{agent_name}' missing tags.")
    return errors

def validate_models():
    errors = []
    for model_name, model_info in MODEL_CATALOG.items():
        if "short_description" not in model_info:
            errors.append(f"Model '{model_name}' missing short_description.")
        if "detailed_description" not in model_info:
            errors.append(f"Model '{model_name}' missing detailed_description.")
        if "tags" not in model_info or not model_info["tags"]:
            errors.append(f"Model '{model_name}' missing tags.")
    return errors

def validate_workflows():
    errors = []
    known_agents = set(AGENT_CATALOG.keys())
    known_models = set(MODEL_CATALOG.keys())

    for root, _, files in os.walk(__workflow_path__):
        for file in files:
            if file.endswith((".yaml", ".yml")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r") as f:
                        workflow = yaml.safe_load(f)

                    steps = workflow.get("steps", [])
                    for step in steps:
                        agent = step.get("agent")
                        model = step.get("model")

                        if agent and agent not in known_agents:
                            errors.append(f"[{path}] Unknown agent: '{agent}'.")

                        if model:
                            if not (model.startswith("${") and model.endswith("}")):
                                if model not in known_models:
                                    errors.append(f"[{path}] Unknown model: '{model}'.")

                except Exception as e:
                    errors.append(f"[{path}] Failed to parse YAML: {e}")
    return errors


def main():
    all_errors = []

    print(Fore.CYAN + "\n🔎 Validating Agents...")
    agent_errors = validate_agents()
    if agent_errors:
        all_errors.extend(agent_errors)
        for e in agent_errors:
            print(Fore.RED + f"❌ {e}")
    else:
        print(Fore.GREEN + "✅ All agents validated successfully.")

    print(Fore.CYAN + "\n🔎 Validating Models...")
    model_errors = validate_models()
    if model_errors:
        all_errors.extend(model_errors)
        for e in model_errors:
            print(Fore.RED + f"❌ {e}")
    else:
        print(Fore.GREEN + "✅ All models validated successfully.")

    print(Fore.CYAN + "\n🔎 Validating Workflows...")
    workflow_errors = validate_workflows()
    if workflow_errors:
        all_errors.extend(workflow_errors)
        for e in workflow_errors:
            print(Fore.RED + f"❌ {e}")
    else:
        print(Fore.GREEN + "✅ All workflows validated successfully.")

    print("\n")
    if all_errors:
        print(Fore.RED + f"❌ Validation failed. {len(all_errors)} issues found.\n")
    else:
        print(Fore.GREEN + "✅ All validations passed successfully. System ready to scale!\n")

if __name__ == "__main__":
    main()
