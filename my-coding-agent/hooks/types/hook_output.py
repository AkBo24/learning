from dataclasses import dataclass
from typing import Any, Dict, Optional

from hooks.types.permission_decision import PermissionDecision


@dataclass(frozen=True)
class HookOutput:
    should_continue: bool = True


@dataclass(frozen=True)
class PreToolUseOutput(HookOutput):
    decision: PermissionDecision = PermissionDecision.ALLOW
    denial_reason: Optional[str] = None             # populated when DENY
    updated_input: Optional[Dict[str, Any]] = None  # populated when MODIFIED
    system_message: Optional[str] = None            # injected into conversation


@dataclass(frozen=True)
class PostMessageSentOutput(HookOutput):
    pass
