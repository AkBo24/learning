from typing import Any, Dict

from tools.delete_file_tool import TOOL as DELETE_FILE_TOOL
from tools.edit_file_tool import TOOL as EDIT_FILE_TOOL
from tools.hooks import (
    AFTER_TOOL_CALL,
    AFTER_TOOL_DECODE,
    AFTER_TOOL_ERROR,
    AFTER_TOOL_SUCCESS,
    BEFORE_TOOL_CALL,
    ToolHookContext,
    emit_hook,
)
from tools.list_files_tool import TOOL as LIST_FILES_TOOL
from tools.read_file_tool import TOOL as READ_FILE_TOOL


TOOL_REGISTRY = {
    READ_FILE_TOOL.name.value: READ_FILE_TOOL,
    LIST_FILES_TOOL.name.value: LIST_FILES_TOOL,
    EDIT_FILE_TOOL.name.value: EDIT_FILE_TOOL,
    DELETE_FILE_TOOL.name.value: DELETE_FILE_TOOL,
}

OPENAI_TOOLS = [tool.config() for tool in TOOL_REGISTRY.values()]


def execute_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    context = ToolHookContext(tool_name=name, raw_args=args)
    emit_hook(BEFORE_TOOL_CALL, context)

    tool = TOOL_REGISTRY.get(name)
    if tool is None:
        error = {
            "error": f"Unknown tool: {name}",
            "tool_name": name,
        }
        context.error = error
        context.finish()
        emit_hook(AFTER_TOOL_ERROR, context)
        emit_hook(AFTER_TOOL_CALL, context)
        return error

    try:
        decoded_params = tool.decode_params(args)
    except Exception as exc:
        error = {
            "error": "Failed to decode tool parameters",
            "tool_name": name,
            "exception_type": type(exc).__name__,
            "message": str(exc),
        }
        context.error = error
        context.exception = exc
        context.finish()
        emit_hook(AFTER_TOOL_ERROR, context)
        emit_hook(AFTER_TOOL_CALL, context)
        return error

    context.decoded_params = decoded_params
    emit_hook(AFTER_TOOL_DECODE, context)

    try:
        result = tool.exec(**decoded_params)
    except Exception as exc:
        error = {
            "error": "Tool execution failed",
            "tool_name": name,
            "exception_type": type(exc).__name__,
            "message": str(exc),
        }
        context.error = error
        context.exception = exc
        context.finish()
        emit_hook(AFTER_TOOL_ERROR, context)
        emit_hook(AFTER_TOOL_CALL, context)
        return error

    context.result = result
    context.finish()
    emit_hook(AFTER_TOOL_SUCCESS, context)
    emit_hook(AFTER_TOOL_CALL, context)
    return result
