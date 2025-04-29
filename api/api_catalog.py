# api/api_catalog.py

API_CATALOG = [
    {
        "path": "/workflow",
        "method": "GET",
        "description": "List all available workflow YAML files",
        "auth": True
    },
    {
        "path": "/workflow/{name}",
        "method": "GET",
        "description": "Get the content of a specific workflow file",
        "auth": True
    },
    {
        "path": "/workflow",
        "method": "POST",
        "description": "Run a workflow from an existing file",
        "auth": True,
        "body": {
            "workflow_file": "Path to a YAML file inside workflows folder"
        }
    },
    {
        "path": "/workflow/inline",
        "method": "POST",
        "description": "Run a workflow from raw YAML sent in the request body",
        "auth": True,
        "body": {
            "workflow_yaml": "YAML workflow definition as a string"
        }
    }
]
