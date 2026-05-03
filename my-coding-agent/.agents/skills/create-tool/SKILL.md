---
name: create-tool
description: Create a new tool this coding agent can invoke
---

Tools are functions that this coding agent can invoke. Currently, all tools are functions. Tools exist in the `/tools` directory.

## Structure

```
tools/
  const/
    tool_registry.py   # imports tool modules, builds TOOL_REGISTRY, exposes execute_tool()
  enum/
    tool_names.py      # canonical ToolName enum values
  hooks/               # lifecycle hooks and logging for tool execution
  types/
    tool.py            # Tool dataclass and OpenAI function config adapter
  utils/               # shared helpers used by tools
  read_file_tool.py    # tool module example
  ...
```

Tool modules live directly under `tools/` and conventionally use the
`<tool_name>_tool.py` filename pattern.

## Create a new tool

1. Add the new tool name to `/tools/enum/tool_names.py`
2. Create the actual tool under `/tools/<tool_name>_tool.py`. Copy the following format and rename `MY_TOOL` / descriptions for the new tool. Keep the main execution function named `exec_tool`:

```py
from typing import Any, Dict

from tools.enum.tool_names import ToolName
from tools.types import Tool
# Add any other imports here.

DESCRIPTION = "Describe what this tool does."

# Parameters use the OpenAI function-tool JSON schema shape.
PARAMETERS = {
    "type": "object",
    "properties": {
        "path": {
            "type": "string",
            "description": "Path used by the tool.",
        },
    },
    "required": ["path"],
}


def exec_tool(path: str) -> Dict[str, Any]:
    # Main implementation.
    return {
        "path": path,
        "action": "completed",
    }


def decode_params(args: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "path": args.get("path", "."),
    }


TOOL = Tool(
    name=ToolName.MY_TOOL,
    description=DESCRIPTION,
    parameters=PARAMETERS,
    exec=exec_tool,
    decode_params=decode_params,
)
```

The keys returned by `decode_params()` must exactly match the execution
function's parameter names. `execute_tool()` calls tools as
`tool.exec(**decoded_params)`.

3. Register the new tool in `/tools/const/tool_registry.py`:
    - import the module's `TOOL` constant with a clear alias
    - add the alias to `TOOL_REGISTRY` using `TOOL.name.value` as the key
4. Test the new tool by compiling the project:

```bash
python -m compileall main.py tools
```

## Notes for agents

- Keep tool return values JSON-serializable dictionaries.
- Keep `PARAMETERS["required"]` aligned with keys in `PARAMETERS["properties"]`.
- Prefer existing helpers such as `tools.utils.resolve_abs_path` for shared utilities. Search this directory for any utils that can be used in the new tool.
- Handle expected failure cases inside the tool when they are part of normal behavior.
  Unexpected exceptions are caught by `execute_tool()` and logged through hooks.
- Do not edit generated files in `tools/**/__pycache__/`.
