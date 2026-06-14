from typing import Any, Dict

from tools.types import Tool, ToolName
from tools.utils import resolve_abs_path


DESCRIPTION = "Deletes a file at the provided path."

PARAMETERS = {
    "type": "object",
    "properties": {
        "path": {
            "type": "string",
            "description": "The path to the file to delete.",
        },
    },
    "required": ["path"],
}


def exec_tool(path: str) -> Dict[str, Any]:
    """
    Deletes a file at the provided path.
    :param path: The path to the file to delete.
    :return: A dictionary with the path and action taken.
    """
    full_path = resolve_abs_path(path)

    if not full_path.exists():
        return {
            "path": str(full_path),
            "action": "file not found",
        }

    if not full_path.is_file():
        return {
            "path": str(full_path),
            "action": "not a file",
        }

    full_path.unlink()
    return {
        "path": str(full_path),
        "action": "deleted",
    }


def decode_params(args: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "path": args.get("path", "."),
    }


TOOL = Tool(
    name=ToolName.DELETE_FILE,
    description=DESCRIPTION,
    parameters=PARAMETERS,
    exec=exec_tool,
    decode_params=decode_params,
)
