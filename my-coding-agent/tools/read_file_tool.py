from typing import Any, Dict

from tools.types import Tool, ToolName
from tools.utils import resolve_abs_path


DESCRIPTION = "Gets the full content of a file provided by the user."

PARAMETERS = {
    "type": "object",
    "properties": {
        "filename": {
            "type": "string",
            "description": "The name of the file to read.",
        },
    },
    "required": ["filename"],
}


def exec_tool(filename: str) -> Dict[str, Any]:
    """
    Gets the full content of a file provided by the user.
    :param filename: The name of the file to read.
    :return: The full content of the file.
    """
    full_path = resolve_abs_path(filename)
    print(full_path)
    with open(str(full_path), "r") as f:
        content = f.read()
    return {
        "file_path": str(full_path),
        "content": content,
    }


def decode_params(args: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "filename": args.get("filename", "."),
    }


TOOL = Tool(
    name=ToolName.READ_FILE,
    description=DESCRIPTION,
    parameters=PARAMETERS,
    exec=exec_tool,
    decode_params=decode_params,
)
