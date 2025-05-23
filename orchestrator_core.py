import yaml, importlib
import re
import os
import time
from utils.printer import Printer
from utils.json_util import render_template 

from models.model_registry import MODEL_REGISTRY

from agents.agent_registry import AGENT_REGISTRY
from agents.code.go_crud_agent import GoCRUDAgent
from agents.code.go_crud_data_agent import GoCRUDDataAgent
from agents.code.go_swagger_agent import GoSwaggerAgent
from agents.audio.audio_agent import AudioAgent
from agents.audio.audio_segmented_agent import SegmentedAudioAgent
from agents.orchestratoragent import OrchestratorAgent
from agents.chat_agent import ChatAgent
from agents.rag.database_updater_agent import RAGDatabaseUpdaterAgent
from agents.rag.attach_agent import RAGAttachAgent
from agents.rag.database_builder_agent import RAGDatabaseBuilderAgent
from agents.rag.query_agent import RAGQueryAgent
from agents.code.angularapp_agent import AngularAppAgent
from agents.images.segmented_image_agent import SegmentedImageAgent
from agents.images.image_agent import ImageAgent
from agents.validators.script_structure_validator_agent import ScriptStructureValidatorAgent
from agents.validators.script_feedback_validator_agent import ScriptFeedbackValidatorAgent
from agents.images.image_analysis_agent import ImageAnalysisAgent
from models.openai.model_gpt_image_1 import ModelGptImage1

from config import debug
from prompt_loader import PromptLoader

def resolve_vars_original(obj, variables: dict):
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

def resolve_vars(obj, variables: dict):
    pattern = re.compile(r"\$\{(.*?)\}")

    if isinstance(obj, dict):
        return {k: resolve_vars(v, variables) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [resolve_vars(i, variables) for i in obj]

    elif isinstance(obj, str):
        matches = pattern.findall(obj)
        for match in matches:
            value = variables.get(match, os.getenv(match))
            if value is not None:
                obj = obj.replace(f"${{{match}}}", str(value))
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


def handle_result(step_name: str, result: dict):
    if not result:
        print(f"⚠️ Step '{step_name}' returned no result (None or empty).")
        return
    print(result)
    if "error" in result:
        print(f"❌ Error in {step_name}: {result['error']}")
    elif "analysis" in result:
        print(f"🧠 Analysis result for '{step_name}':\n{result['analysis']}")
    elif "image_path" in result:
        print(f"🖼️ Image saved: {result['image_path']}")
    elif "video_path" in result:
        print(f"🎬 Video saved: {result['video_path']}")
    elif "subtitle_path" in result:
        print(f"📝 Subtitle file: {result['subtitle_path']}")
    elif "files" in result:
        print(f"📁 Generated files in {step_name}:")
        for k, v in result["files"].items():
            print(f"   - {k}: {v}")
    else:
        print(f"✅ Step '{step_name}' completed with output:")
        print(result)


def load_agent(agent_name: str):
    if agent_name not in AGENT_REGISTRY:
        raise ValueError(f"Unknown agent '{agent_name}'. Check agent_registry.py.")
    return AGENT_REGISTRY[agent_name]()


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
    if agent_name == "ScriptFeedbackValidatorAgent":
        return ScriptFeedbackValidatorAgent(llm,prompt_template)   
    if agent_name == "AudioAgent":
        return AudioAgent(llm)   



def get_rag_agent(agent_name, collection_name, storage_path):
    if agent_name=="RAGDatabaseBuilderAgent": 
        return RAGDatabaseBuilderAgent(collection_name,storage_path)
    if agent_name=="RAGQueryAgent":
        return RAGQueryAgent(collection_name,storage_path)
    if agent_name=="RAGDatabaseUpdaterAgent":
        return RAGDatabaseUpdaterAgent(collection_name,storage_path)


def load_workflow_with_includes(workflow_path, loaded_paths=None):
    """ Recursively loads workflow YAML and included fragments. """
    loaded_paths = loaded_paths or set()
    if workflow_path in loaded_paths:
        raise ValueError(f"Circular include detected with: {workflow_path}")
    loaded_paths.add(workflow_path)

    with open(workflow_path) as f:
        workflow = yaml.safe_load(f)

    steps = workflow.get("steps", [])
    includes = workflow.get("include", [])

    if not isinstance(includes, list):
        includes = [includes]

    for include_file in includes:
        include_path = os.path.join(os.path.dirname(workflow_path), include_file)
        included_workflow = load_workflow_with_includes(include_path, loaded_paths)
        steps = included_workflow["steps"] + steps  # prepend included steps

    workflow["steps"] = steps
    return workflow


def run_workflow(workflow_path, streamlit_mode=False):
    import copy
    start_time = time.time()

    workflow = load_workflow_with_includes(workflow_path)

    vars_dict = workflow.get("vars", {})
    steps = resolve_vars(workflow["steps"], vars_dict)

    results = {}

    for step in steps:
        loop = step.get("loop")
        loop_values = []
        loop_var = None

        if loop:
            loop_var = loop.get("var")
            if "values" in loop:
                loop_values = loop["values"]
            elif "count" in loop:
                loop_values = list(range(1, loop["count"] + 1))
        else:
            loop_values = [None]

        for idx, loop_val in enumerate(loop_values):
            local_step = copy.deepcopy(step)
            name = local_step["name"]
            local_name = f"{name}_{idx+1}" if loop else name

            local_vars = vars_dict.copy()
            if loop_var:
                local_vars[loop_var] = loop_val

            input_spec = resolve_vars(local_step["input"], local_vars)
            inputs = resolve_inputs(input_spec, results, local_vars)

            # 🧠 Evaluate `when` condition (optional)
            when = local_step.get("when", True)
            if isinstance(when, str) and when.startswith("{{"):
                try:
                    context = {**local_vars, **results}
                    rendered_when = render_template(when, context)
                    try:
                        when_result = eval(rendered_when)
                    except Exception as e:
                        Printer.info(f"⚠️ Eval error in step '{local_name}': {e}")
                        when_result = False
                except Exception as e:
                    Printer.info(f"⚠️ Failed to evaluate 'when' for step '{local_name}': {e}")
                    when_result = False
            else:
                when_result = bool(when)

            if not when_result:
                Printer.info(f"⏭ Skipping step '{local_name}' due to 'when: {when}'")
                results[local_name] = {"status": "Skipped", "details": f"when={when}"}
                continue

            step_type = local_step["type"]
            agent_name = local_step["agent"]

            if step_type == "ai":
                template_name = local_step.get("template_name", "default")
                temperature = local_step.get("temperature", 0.2)
                model = local_step["model"]
                llm = get_model(model, temperature)
                agent = get_ai_agent(llm, agent_name, template_name)
                if not streamlit_mode:
                    print(f"▶️ {local_name} using {agent_name}")
                output = agent.run(**inputs)
                results[local_name] = output
                handle_result(local_name, output)

            elif step_type == "validator":
                agent = globals()[agent_name]()
                output = agent.validate(**inputs)
                results[local_name] = output
                handle_result(local_name, output)

            elif step_type == "ai-image":
                if agent_name == "ImageAgent":
                    model = local_step["model"]
                    temperature = local_step.get("temperature", 0.2)
                    llm = get_model(model, temperature)
                    agent = ImageAgent(llm)
                    result = agent.run(**inputs)
                elif agent_name == "ImageAnalysisAgent":
                    temperature = local_step.get("temperature", 0.2)
                    model = ModelGptImage1(temperature)
                    agent = ImageAnalysisAgent(model)
                    result = agent.run(**inputs)
                elif agent_name == "SegmentedImageAgent":
                    agent = SegmentedImageAgent()
                    result = agent.run(**inputs)
                else:
                    raise ValueError(f"Unknown ai-image agent '{agent_name}'")
                results[local_name] = result
                handle_result(local_name, result)

            elif step_type == "ai-audio":
                if agent_name == "AudioAgent":
                    model_name = local_step.get("model")
                    if model_name not in MODEL_REGISTRY:
                        raise ValueError(f"Unknown model '{model_name}'")
                    model_instance = MODEL_REGISTRY[model_name]()
                    agent = AudioAgent(model_instance)
                elif agent_name == "SegmentedAudioAgent":
                    agent = SegmentedAudioAgent()
                output = agent.run(**inputs)
                results[local_name] = output
                handle_result(local_name, output)

            elif step_type == "rag":
                agent = get_rag_agent(agent_name, local_step["collection_name"], local_step["storage_path"])
                if not streamlit_mode:
                    print(f"▶️ {local_name} using {agent_name}")
                output = agent.run(**inputs)
                results[local_name] = output
                handle_result(local_name, output)

            else:
                agent = load_agent(agent_name)
                if not streamlit_mode:
                    print(f"▶️ {local_name} using {agent_name}")
                output = agent.run(**inputs)
                results[local_name] = output
                handle_result(local_name, output)

    duration = round(time.time() - start_time, 2)
    if not streamlit_mode:
        print(f"\n✅ Workflow completed in {duration} seconds.")
    else:
        results["_execution_duration"] = duration

    return results



def run_workflow_original(workflow_path, streamlit_mode=False):
    start_time = time.time()

    # with open(workflow_path) as f:
    #     workflow = yaml.safe_load(f)
    workflow = load_workflow_with_includes(workflow_path)

    vars_dict = workflow.get("vars", {})
    steps = resolve_vars(workflow["steps"], vars_dict)

    results = {}

    for step in steps:
        name, step_type, agent_name = step["name"], step["type"], step["agent"]
        input_spec = resolve_vars(step["input"], vars_dict)
        inputs = resolve_inputs(input_spec, results, vars_dict)
        
        # 🧠 Evaluate `when` condition (optional)
        when = step.get("when", True)
        if isinstance(when, str) and when.startswith("{{"):
            try:
                context = {**vars_dict, **results}  # merge vars + step results
                rendered_when = render_template(when, context)
                try:
                    when_result = eval(rendered_when)
                except Exception as e:
                    Printer.info(f"⚠️ Eval error in step '{name}': {e}")
                    when_result = False

            except Exception as e:
                Printer.info(f"⚠️ Failed to evaluate 'when' for step '{name}': {e}")
                when_result = False
        else:
            when_result = bool(when)

        if not when_result:
            Printer.info(f"⏭ Skipping step '{name}' due to 'when: {when}'")
            results[name] = {"status": "Skipped", "details": f"when={when}"}
            continue

        if step_type == "ai":
            template_name = step.get("template_name", "default")
            temperature = step.get("temperature", 0.2)
            model = step["model"]
            llm = get_model(model, temperature)
            agent = get_ai_agent(llm, agent_name, template_name)
            if not streamlit_mode:
                print(f"▶️ {name} using {agent_name}")
            output = agent.run(**inputs)
            results[name] = output
            handle_result(name, output)

        elif step_type == "validator":
            agent = globals()[agent_name]()
            output = agent.validate(**inputs)
            results[name] = output
            handle_result(name, output)

        elif step_type == "ai-image":
            if agent_name == "ImageAgent":
                model = step["model"]
                temperature = step.get("temperature", 0.2)
                llm = get_model(model, temperature)
                agent = ImageAgent(llm)
                result = agent.run(**inputs)
            elif agent_name == "ImageAnalysisAgent":
                temperature = step.get("temperature", 0.2)
                model = ModelGptImage1(temperature)
                agent = ImageAnalysisAgent(model)
                result = agent.run(**inputs)
            elif agent_name == "SegmentedImageAgent":
                agent = SegmentedImageAgent()
                result = agent.run(**inputs)
            else:
                raise ValueError(f"Unknown ai-image agent '{agent_name}'")
            results[name] = result
            handle_result(name, result)

        elif step_type == "ai-audio":
            if agent_name == "AudioAgent":
                model_name = step.get("model")
                if model_name not in MODEL_REGISTRY:
                    raise ValueError(f"Unknown model '{model_name}'")
                model_instance = MODEL_REGISTRY[model_name]()
                agent = AudioAgent(model_instance)
            elif agent_name == "SegmentedAudioAgent":
                agent = SegmentedAudioAgent()
            output = agent.run(**inputs)
            results[name] = output
            handle_result(name, output)

        elif step_type == "rag":
            agent = get_rag_agent(agent_name, step["collection_name"], step["storage_path"])
            if not streamlit_mode:
                print(f"▶️ {name} using {agent_name}")
            output = agent.run(**inputs)
            results[name] = output
            handle_result(name, output)

        else:
            agent = load_agent(agent_name)
            if not streamlit_mode:
                print(f"▶️ {name} using {agent_name}")
            output = agent.run(**inputs)
            results[name] = output
            handle_result(name, output)

    duration = round(time.time() - start_time, 2)
    if not streamlit_mode:
        print(f"\n✅ Workflow completed in {duration} seconds.")
    else:
        results["_execution_duration"] = duration

    return results

