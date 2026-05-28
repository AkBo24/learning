from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class HookInput:
    session_id: str
    cwd: str
    hook_name: str

@dataclass(frozen=True)
class PreToolUseInput(HookInput):
    tool_name: str
    tool_input: Dict[str, Any]
    tool_use_id: str
