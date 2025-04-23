import yaml, importlib
import re
from utils.printer import Printer
from models.modelgpt35turbo import ModelGpt35Turbo, ModelGpt4, ModelGpt4Turbo
from models.modellocalollama import ModelOllama
from agents.goswaggeragent import GoSwaggerAgent, GoCRUDAgent
from agents.chatagent import ChatAgent
from agents.rag import RAGDatabaseBuilderAgent, RAGQueryAgent, RAGDatabaseUpdaterAgent
from agents.angularappagent import AngularAppAgent
from config import debug
from prompt_loader import PromptLoader

def resolve_vars(obj, variables: dict):
    pattern = re.compile(r"\$\{(.*?)\}")

    if isinstance(obj, dict):
        return {k: resolve_vars(v, variables) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [resolve_vars(i, variables) for i in obj]

    elif isinstance(obj, str):
        matches = pattern.findall(obj)
        for match in matches:
            if match in variables:
                obj = obj.replace(f"${{{match}}}", variables[match])
        return obj

    return obj  # Return original type (int, bool, etc.)


def resolve_inputs(input_dict, context, variables=None):
    resolved = {}
    variables = variables or {}

    jinja_pattern = re.compile(r"{{\s*([^}]+)\s*}}")
    var_pattern = re.compile(r"^\${(\w+)}$")  # matches full strings like ${var}

    for key, val in input_dict.items():
        if isinstance(val, str):

            # Case 1: "${my_var}" format → from variables
            var_match = var_pattern.match(val)
            if var_match:
                var_name = var_match.group(1)
                resolved[key] = variables.get(var_name)
                continue

            # Case 2: "{{ var }}" or "{{ step.result }}" → Jinja-style resolution
            if "{{" in val and "}}" in val:
                def replace(match):
                    expr = match.group(1).strip()
                    if "." in expr:
                        step_name, field = expr.split(".", 1)
                        return str(context.get(step_name, {}).get(field, ""))
                    else:
                        return str(variables.get(expr, ""))
                resolved[key] = jinja_pattern.sub(replace, val)
                continue

            # Case 3: Dot-notation step references (e.g., step_name.output)
            if val.count(".") == 1 and not val.startswith("./") and "/" not in val:
                step, field = val.split(".")
                # Check if it's a real reference — otherwise treat as literal
                if step in context and field in context[step]:
                    resolved[key] = context[step][field]
                    continue

            # Case 4: Fallback — treat as literal string
            resolved[key] = val

        else:
            # Non-string input, just use as-is
            resolved[key] = val

    return resolved


def resolve_inputs_original(input_dict, context, variables=None):
    resolved = {}
    variables = variables or {}

    # Regex patterns
    jinja_pattern = re.compile(r"{{\s*([^}]+)\s*}}")
    var_pattern = re.compile(r"^\${(\w+)}$")  # full match for ${var}

    for key, val in input_dict.items():
        if isinstance(val, str):

            # Case 1: Exact variable match (${var})
            var_match = var_pattern.match(val)
            if var_match:
                var_name = var_match.group(1)
                resolved[key] = variables.get(var_name)

            # Case 2: Pure dot notation (step.output) — strict match
            elif val.count(".") == 1 and not val.startswith("./") and "/" not in val:
                step, field = val.split(".")
                resolved[key] = context.get(step, {}).get(field)

            # Case 3: Jinja-style expression(s) — can be embedded in strings
            elif "{{" in val and "}}" in val:
                def replace_jinja(match):
                    expr = match.group(1).strip()
                    if "." in expr:
                        step, field = expr.split(".", 1)
                        return str(context.get(step, {}).get(field, ""))
                    else:
                        return str(variables.get(expr, ""))
                resolved[key] = jinja_pattern.sub(replace_jinja, val)

            # Case 4: Literal string
            else:
                resolved[key] = val

        else:
            # Not a string — pass through unchanged
            resolved[key] = val

    return resolved

def load_agent(agent_name):

    modules = [
        "agents.requirements_extractor",
        "agents.github_integration",
        "agents.goswaggeragent",
        "agents.chatagent",
        "agents.file_system",
        "agents.rag",
        "agents.gocrudagent",
        "agents.angularappagent"

    ]
    for mod in modules:
        module = importlib.import_module(mod)
        if hasattr(module, agent_name):
            return getattr(module, agent_name)()
    raise ImportError(f"Agent {agent_name} not found.")

def get_model(model_name):
    if model_name=="ModelGpt35Turbo":   
        return ModelGpt35Turbo()
    if model_name=="ModelOllama":   
        return ModelOllama()
    if model_name == "ModelGpt4":
        return ModelGpt4()
    if model_name == "ModelGpt4Turbo":
        return ModelGpt4Turbo()

def get_ai_agent(llm, agent_name, name="default"):
    prompt_loader = PromptLoader()
    prompt_template = prompt_loader.load_prompt(agent_name, name)
    
    if agent_name=="GoSwaggerAgent": 
        return GoSwaggerAgent(llm, prompt_template)
    if agent_name=="ChatAgent":   
        return ChatAgent(llm,prompt_template)
    if agent_name=="GoCRUDAgent":
        return GoCRUDAgent(llm=llm, prompt_template=prompt_template)
    if agent_name=="AngularAppAgent":   
        return AngularAppAgent(llm,prompt_template)

        



def get_rag_agent(agent_name, collection_name, storage_path):
    if agent_name=="RAGDatabaseBuilderAgent": 
        return RAGDatabaseBuilderAgent(collection_name,storage_path)
    if agent_name=="RAGQueryAgent":
        return RAGQueryAgent(collection_name,storage_path)
    if agent_name=="RAGDatabaseUpdaterAgent":
        return RAGDatabaseUpdaterAgent(collection_name,storage_path)



def run_workflow(workflow_path, streamlit_mode=False):
    with open(workflow_path) as f:
        workflow = yaml.safe_load(f)

    vars_dict = workflow.get("vars", {})
    steps = resolve_vars(workflow["steps"], vars_dict)

    results = {}

    for step in steps: # workflow["steps"]:
        name, step_type, agent_name = step["name"], step["type"], step["agent"]
        input_spec = resolve_vars(step["input"], vars_dict)
        inputs = resolve_inputs(input_spec, results, vars_dict)

        print(inputs)

        if step_type == "ai":
            template_name = step.get("template_name", "default")
            model = step["model"]   
            llm = get_model(model)
            agent = get_ai_agent(llm, agent_name, template_name)
            if not streamlit_mode:
                print(f"▶️ {name} using {agent_name}")
            output = agent.run(**inputs)
            results[name] = output
            if(debug):
                print(output)

        elif step_type == "rag":
            agent = get_rag_agent(agent_name, step["collection_name"], step["storage_path"])
            if not streamlit_mode:
                print(f"▶️ {name} using {agent_name}")
            output = agent.run(**inputs)
            results[name] = output
            if(debug):
                print(output)
        else: 
            agent = load_agent(agent_name)

            if not streamlit_mode:
                print(f"▶️ {name} using {agent_name}")
            output = agent.run(**inputs)
            results[name] = output
            if(debug):
                print(output)

    return results
