import os

# 🔧 Config
PYTHON_OUTPUT = "python_code_completed.txt"
YAML_OUTPUT = "yaml_code_completed.txt"
WORKFLOW_DIR = "workflows"
EXCLUDE_PY_FILES = {"config.py", "secrets.py", "test_ignore.py", "collect.py"}
EXCLUDE_PY_DIRS = {".venv", "venv", "__pycache__"}
EXCLUDE_YAML_FILES = set()

def collect_python_code(base_dir="."):
    output_lines = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_PY_DIRS]
        for file in files:
            if file.endswith(".py") and file not in EXCLUDE_PY_FILES:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        code = f.read()
                except UnicodeDecodeError:
                    try:
                        with open(full_path, "r", encoding="latin-1") as f:
                            code = f.read()
                    except Exception as e:
                        print(f"⚠️ Failed to read {full_path}: {e}")
                        continue
                rel_path = os.path.relpath(full_path, base_dir)
                output_lines.append(f"{rel_path}\n===\n{code}\n===\n")
    return output_lines

def collect_yaml_files(base_dir=WORKFLOW_DIR):
    output_lines = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith((".yaml", ".yml")) and file not in EXCLUDE_YAML_FILES:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    rel_path = os.path.relpath(full_path, base_dir)
                    output_lines.append(f"{rel_path}\n===\n{content}\n===\n")
                except Exception as e:
                    print(f"⚠️ Failed to read {full_path}: {e}")
    return output_lines

def write_output():
    with open(PYTHON_OUTPUT, "w", encoding="utf-8") as py_out:
        py_lines = collect_python_code()
        py_out.writelines(py_lines)
        print(f"✅ Python code saved to {PYTHON_OUTPUT}")

    with open(YAML_OUTPUT, "w", encoding="utf-8") as yaml_out:
        yaml_lines = collect_yaml_files()
        yaml_out.writelines(yaml_lines)
        print(f"✅ YAML workflows saved to {YAML_OUTPUT}")

if __name__ == "__main__":
    write_output()
