from enum import Enum


class HookEvent(str, Enum):
    PRE_TOOL_USE = "pre_tool_use"