📄 workflows.md

Workflows Deep Dive

YAML format

vars: section for shared variables

steps: list for ordered execution

Patterns Supported:

${var} - variable replacement

step_name.result - access previous output

{{ var }} - Jinja-style variable resolution

Examples:

CRUD generation

Angular frontend scaffolding

GitHub PR automation