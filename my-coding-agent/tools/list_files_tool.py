from typing import Any, Dict

from tools.enum.tool_names import ToolName
from tools.types import Tool
from tools.utils import resolve_abs_path


DESCRIPTION = "Lists the files in a directory provided by the user."

PARAMETERS = {
    "type": "object",
    "properties": {
        "path": {
            "type": "string",
            "description": "The path to a directory to list files from.",
        },
    },
    "required": ["path"],
}


def list_files(path: str) -> Dict[str, Any]:
    """
    Lists the files in a directory provided by the user.
    :param path: The path to a directory to list files from.
    :return: A list of files in the directory.
    """
    full_path = resolve_abs_path(path)
    all_files = []
    for item in full_path.iterdir():
        all_files.append({
            "filename": item.name,
            "type": "file" if item.is_file() else "dir",
        })
    return {
        "path": str(full_path),
        "files": all_files,
    }


def decode_params(args: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "path": args.get("path", "."),
    }


TOOL = Tool(
    name=ToolName.LIST_FILES,
    description=DESCRIPTION,
    parameters=PARAMETERS,
    exec=list_files,
    decode_params=decode_params,
)
