from typing import Any, Dict

from tools.enum.tool_names import ToolName
from tools.types import Tool
from tools.utils import resolve_abs_path


DESCRIPTION = (
    "Replaces first occurrence of old_str with new_str in file. If old_str is "
    "empty, create/overwrite file with new_str."
)

PARAMETERS = {
    "type": "object",
    "properties": {
        "path": {
            "type": "string",
            "description": "The path to the file to edit.",
        },
        "old_str": {
            "type": "string",
            "description": "The string to replace.",
        },
        "new_str": {
            "type": "string",
            "description": "The string to replace with.",
        },
    },
    "required": ["path", "old_str", "new_str"],
}


def edit_file(path: str, old_str: str, new_str: str) -> Dict[str, Any]:
    """
    Replaces first occurrence of old_str with new_str in file. If old_str is empty,
    create/overwrite file with new_str.
    :param path: The path to the file to edit.
    :param old_str: The string to replace.
    :param new_str: The string to replace with.
    :return: A dictionary with the path to the file and the action taken.
    """
    full_path = resolve_abs_path(path)
    if old_str == "":
        full_path.write_text(new_str, encoding="utf-8")
        return {
            "path": str(full_path),
            "action": "created_file",
        }
    original = full_path.read_text(encoding="utf-8")
    if original.find(old_str) == -1:
        return {
            "path": str(full_path),
            "action": "old_str not found",
        }
    edited = original.replace(old_str, new_str, 1)
    full_path.write_text(edited, encoding="utf-8")
    return {
        "path": str(full_path),
        "action": "edited",
    }


def decode_params(args: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "path": args.get("path", "."),
        "old_str": args.get("old_str", ""),
        "new_str": args.get("new_str", ""),
    }


TOOL = Tool(
    name=ToolName.EDIT_FILE,
    description=DESCRIPTION,
    parameters=PARAMETERS,
    exec=edit_file,
    decode_params=decode_params,
)
