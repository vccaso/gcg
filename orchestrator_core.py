import yaml, importlib
import re
from utils.printer import Printer
from models.modelgpt35turbo import ModelGpt35Turbo
from models.modellocalollama import ModelOllama
from agents.goswaggeragent import GoSwaggerAgent
from agents.chatagent import ChatAgent

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


def load_agent(agent_name):
    modules = [
        "agents.requirements_extractor",
        "agents.github_integration",
        "agents.goswaggeragent",
        "agents.chatagent",
        "agents.file_system",
        "agents.rag"

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

def get_agent(llm, agent_name):
    if agent_name=="GoSwaggerAgent": 
        return GoSwaggerAgent(llm, "You are an expert Go programmer specialized in OpenAPI (Swagger) documentation. Please analyze the following Go code and insert the appropriate swagger-compatible comment blocks (e.g., @Summary, @Description, @Param, @Success, etc.) for each function, struct, and endpoint. Preserve all existing code exactly as it is; do not remove or alter the package declaration, import statements, or any other lines. Only add Swagger comments where relevant. Return only the updated code with the new Swagger documentation.\n\n```go\n{original_code}\n``")
    if agent_name=="ChatAgent":   
        return ChatAgent(llm,"You are a helpful assistant.")


def run_workflow(workflow_path, streamlit_mode=False):
    with open(workflow_path) as f:
        workflow = yaml.safe_load(f)

    vars_dict = workflow.get("vars", {})
    steps = resolve_vars(workflow["steps"], vars_dict)

    results = {}

    for step in steps: # workflow["steps"]:
        name, step_type, agent_name, input_spec = step["name"], step["type"], step["agent"], step["input"]
        inputs = {k: results.get(v, v) for k, v in input_spec.items()}
        # Printer.success(inputs)
        if step_type == "ai":
            model = step["model"]   
            llm = get_model(model)
            agent = get_agent(llm, agent_name)
            if not streamlit_mode:
                print(f"▶️ {name} using {agent_name}")
            output = agent.run(**inputs)
            results[name] = output
            print(output)

        # elif step_type == "git":
        else: 
            agent = load_agent(agent_name)

            if not streamlit_mode:
                print(f"▶️ {name} using {agent_name}")
            output = agent.run(**inputs)
            results[name] = output
            print(output)

    return results
