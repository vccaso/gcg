import yaml, importlib
import re
from utils.printer import Printer
from models.modelgpt35turbo import ModelGpt35Turbo
from models.modellocalollama import ModelOllama
from agents.goswaggeragent import GoSwaggerAgent, GoCRUDAgent
from agents.chatagent import ChatAgent
from agents.rag import RAGDatabaseBuilderAgent, RAGQueryAgent, RAGDatabaseUpdaterAgent
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

    for key, val in input_dict.items():
        if isinstance(val, str):

            # ✅ Case 1: Variable placeholder like ${my_var}
            if val.startswith("${") and val.endswith("}"):
                var_name = val[2:-1]
                resolved[key] = variables.get(var_name)

            # ✅ Case 2: Step output reference (dot notation) with NO slash or path
            elif "." in val and not val.startswith("./") and not "/" in val:
                parts = val.split(".")
                result = context
                for part in parts:
                    result = result.get(part)
                    if result is None:
                        break
                resolved[key] = result

            # ✅ Case 3: Already a normal literal string
            else:
                resolved[key] = val

        else:
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
        "agents.gocrudagent"

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

def get_ai_agent(llm, agent_name):
    prompt_loader = PromptLoader()
    if agent_name=="GoSwaggerAgent": 
        return GoSwaggerAgent(llm, "You are an expert Go programmer specialized in OpenAPI (Swagger) documentation. Please analyze the following Go code and insert the appropriate swagger-compatible comment blocks (e.g., @Summary, @Description, @Param, @Success, etc.) for each function, struct, and endpoint. Preserve all existing code exactly as it is; do not remove or alter the package declaration, import statements, or any other lines. Only add Swagger comments where relevant. Return only the updated code with the new Swagger documentation.\n\n```go\n{original_code}\n``")
    if agent_name=="ChatAgent":   
        return ChatAgent(llm,"You are a helpful assistant.")
    if agent_name=="GoCRUDAgent":
        prompt = prompt_loader.load_prompt(agent_name)
        return GoCRUDAgent(llm=llm, prompt_template=prompt)



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
        if step_type == "ai":
            model = step["model"]   
            llm = get_model(model)
            agent = get_ai_agent(llm, agent_name)
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
