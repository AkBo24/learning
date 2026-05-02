from typing import Any, Dict

from tools.edit_file_tool import TOOL as EDIT_FILE_TOOL
from tools.list_files_tool import TOOL as LIST_FILES_TOOL
from tools.read_file_tool import TOOL as READ_FILE_TOOL


TOOL_REGISTRY = {
    READ_FILE_TOOL.name.value: READ_FILE_TOOL,
    LIST_FILES_TOOL.name.value: LIST_FILES_TOOL,
    EDIT_FILE_TOOL.name.value: EDIT_FILE_TOOL,
}

OPENAI_TOOLS = [tool.config() for tool in TOOL_REGISTRY.values()]


def execute_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    tool = TOOL_REGISTRY.get(name)
    if tool is None:
        return {
            "error": f"Unknown tool: {name}",
            "tool_name": name,
        }

    decoded_params = tool.decode_params(args)
    return tool.exec(**decoded_params)
