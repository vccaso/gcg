import yaml, importlib
import re
import time
from utils.printer import Printer


from models.model_registry import MODEL_REGISTRY

from agents.agent_registry import AGENT_REGISTRY
from agents.go_crud_agent import GoCRUDAgent
from agents.go_crud_data_agent import GoCRUDDataAgent
from agents.go_swagger_agent import GoSwaggerAgent
from agents.dalle3_agent import Dalle3Agent
from agents.dalle2_agent import Dalle2Agent
from agents.audio.audio_agent import AudioAgent
from agents.audio.audio_segmented_agent import SegmentedAudioAgent
from agents.orchestratoragent import OrchestratorAgent
from agents.chat_agent import ChatAgent
from agents.rag.database_updater_agent import RAGDatabaseUpdaterAgent
from agents.rag.attach_agent import RAGAttachAgent
from agents.rag.database_builder_agent import RAGDatabaseBuilderAgent
from agents.rag.query_agent import RAGQueryAgent
from agents.angularapp_agent import AngularAppAgent
from agents.images.segmented_image_agent import SegmentedImageAgent


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
                obj = obj.replace(f"${{{match}}}", str(variables[match]))
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
                        # return str(context.get(step_name, {}).get(field, ""))
                        step_result = context.get(step_name)
                        if isinstance(step_result, dict):
                            return str(step_result.get(field, ""))
                        return str(step_result) if field == "result" else ""
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


def load_agent(agent_name: str):
    if agent_name not in AGENT_REGISTRY:
        raise ValueError(f"Unknown agent '{agent_name}'. Check agent_registry.py.")
    return AGENT_REGISTRY[agent_name]()

def load_agent_old(agent_name):

    modules = [
        "agents.requirements_extractor",
        "agents.github_integration",
        "agents.gocodeagent",
        "agents.chatagent",
        "agents.file_system",
        "agents.rag",
        "agents.gocrudagent",
        "agents.angularappagent",
        "agents.orchestratoragent"

    ]
    for mod in modules:
        module = importlib.import_module(mod)
        if hasattr(module, agent_name):
            return getattr(module, agent_name)()
    raise ImportError(f"Agent {agent_name} not found.")




def get_model(model_name: str, temperature):
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model '{model_name}'")
    return MODEL_REGISTRY[model_name](temperature)


def get_ai_agent(llm, agent_name, name="default"):
    prompt_loader = PromptLoader()
    prompt_template = prompt_loader.load_prompt(agent_name, name)
    
    if agent_name == "OrchestratorAgent":
        return OrchestratorAgent(llm, prompt_template)
    if agent_name=="GoSwaggerAgent": 
        return GoSwaggerAgent(llm, prompt_template)
    if agent_name=="ChatAgent":   
        return ChatAgent(llm,prompt_template)
    if agent_name=="GoCRUDAgent":
        return GoCRUDAgent(llm=llm, prompt_template=prompt_template)
    if agent_name=="AngularAppAgent":   
        return AngularAppAgent(llm,prompt_template)  
    if agent_name == "GoCRUDDataAgent":
        return GoCRUDDataAgent(llm,prompt_template)   



def get_rag_agent(agent_name, collection_name, storage_path):
    if agent_name=="RAGDatabaseBuilderAgent": 
        return RAGDatabaseBuilderAgent(collection_name,storage_path)
    if agent_name=="RAGQueryAgent":
        return RAGQueryAgent(collection_name,storage_path)
    if agent_name=="RAGDatabaseUpdaterAgent":
        return RAGDatabaseUpdaterAgent(collection_name,storage_path)



def run_workflow(workflow_path, streamlit_mode=False):
    start_time = time.time()

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
            template_name = step.get("template_name", "default")
            temperature = step.get("temperature",0.2)
            model = step["model"]   
            llm = get_model(model, temperature)
            agent = get_ai_agent(llm, agent_name, template_name)
            if not streamlit_mode:
                print(f"▶️ {name} using {agent_name}")
            output = agent.run(**inputs)
            results[name] = output
            if(debug):
                print(f"[DEBUG] Step '{name}' result:", output)

        elif step_type == "ai-image":
            if agent_name == "Dalle2Agent":
                agent = Dalle2Agent()
                result = agent.generate_image(**inputs)
            elif agent_name == "Dalle3Agent":
                agent = Dalle3Agent()
                result = agent.generate_image(**inputs)
            elif agent_name == "SegmentedImageAgent":
                agent = SegmentedImageAgent()
                result = agent.run(**inputs)
            else:
                raise ValueError(f"Unknown ai-image agent '{agent_name}'")

            # 🖼 Output handling
            if "url" in result:
                print("Image URL:", result["url"])
            elif "images" in result:
                print("Generated images:")
                for section, url in result["images"].items():
                    print(f"  {section}: {url}")
            elif "error" in result:
                print("Error:", result["error"])
            else:
                print("Unexpected result format:", result)


        elif step_type == "ai-audio":
            if agent_name=="AudioAgent":
                agent = AudioAgent()
            if agent_name=="SegmentedAudioAgent":
                agent = SegmentedAudioAgent()
            output = agent.run(**inputs)
            results[name] = output
            print(f"[DEBUG] Step '{name}' result:", output)
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

    duration = round(time.time() - start_time, 2)
    if not streamlit_mode:
        print(f"\n✅ Workflow completed in {duration} seconds.")
    else:
        results["_execution_duration"] = duration  # optionally expose it to UI


    return results
