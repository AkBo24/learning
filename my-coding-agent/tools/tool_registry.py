from typing import Any, Dict

from tools.delete_file_tool import TOOL as DELETE_FILE_TOOL
from tools.edit_file_tool import TOOL as EDIT_FILE_TOOL
from tools.list_files_tool import TOOL as LIST_FILES_TOOL
from tools.read_file_tool import TOOL as READ_FILE_TOOL
from tools.run_shell_command_tool import TOOL as RUN_SHELL_COMMAND_TOOL


TOOL_REGISTRY = {
    READ_FILE_TOOL.name.value: READ_FILE_TOOL,
    LIST_FILES_TOOL.name.value: LIST_FILES_TOOL,
    EDIT_FILE_TOOL.name.value: EDIT_FILE_TOOL,
    DELETE_FILE_TOOL.name.value: DELETE_FILE_TOOL,
    RUN_SHELL_COMMAND_TOOL.name.value: RUN_SHELL_COMMAND_TOOL,
}

OPENAI_TOOLS = [tool.config() for tool in TOOL_REGISTRY.values()]


def execute_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    tool = TOOL_REGISTRY.get(name)
    if tool is None:
        return {
            "error": f"Unknown tool: {name}",
            "tool_name": name,
        }

    try:
        decoded_params = tool.decode_params(args)
    except Exception as exc:
        return {
            "error": "Failed to decode tool parameters",
            "tool_name": name,
            "exception_type": type(exc).__name__,
            "message": str(exc),
        }

    try:
        result = tool.exec(**decoded_params)
    except Exception as exc:
        return {
            "error": "Tool execution failed",
            "tool_name": name,
            "exception_type": type(exc).__name__,
            "message": str(exc),
        }

    return result
