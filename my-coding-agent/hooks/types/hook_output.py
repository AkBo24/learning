from dataclasses import dataclass
from typing import Any, Dict, Optional

from hooks.types.permission_decision import PermissionDecision


@dataclass(frozen=True)
class HookOutput:
    decision: PermissionDecision = PermissionDecision.ALLOW
    should_continue: bool = True
    denial_reason: Optional[str] = None             # populated when DENY
    updated_input: Optional[Dict[str, Any]] = None  # populated when MODIFIED
    system_message: Optional[str] = None            # injected into conversation
