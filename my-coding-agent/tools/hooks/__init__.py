from tools.hooks.context import ToolHookContext
from tools.hooks.error_logger import log_tool_error
from tools.hooks.manager import emit_hook, register_hook


BEFORE_TOOL_CALL = "before_tool_call"
AFTER_TOOL_DECODE = "after_tool_decode"
AFTER_TOOL_SUCCESS = "after_tool_success"
AFTER_TOOL_ERROR = "after_tool_error"
AFTER_TOOL_CALL = "after_tool_call"

register_hook(AFTER_TOOL_ERROR, log_tool_error)

__all__ = [
    "AFTER_TOOL_CALL",
    "AFTER_TOOL_DECODE",
    "AFTER_TOOL_ERROR",
    "AFTER_TOOL_SUCCESS",
    "BEFORE_TOOL_CALL",
    "ToolHookContext",
    "emit_hook",
    "register_hook",
]
