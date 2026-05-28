import os
import re
from typing import Callable
from hooks.types import Hook, HookEvent, HookOutput, PermissionDecision, PreToolUseInput
from hooks.log_tool_use import LogToolUse
from hooks.tool_permissions import ToolPermissions

HookCallback = Callable[[dict, str | None], dict]

_HOOK_REGISTRY = {
    HookEvent.PRE_TOOL_USE: [ToolPermissions, LogToolUse]
}
"""
Event: Hook[]

e.g., PreToolUse: [LogToolRequest]
"""

class HookRegistry:
    def __init__(self):
        self._hooks: dict[str, list[Hook]] = _HOOK_REGISTRY

    def run(self, event: HookEvent, tool_name, input_data) -> dict[str, HookOutput]:
        """
        1. Take event, input_data, tool_use_id
        2. Get hooks registered for the event
        3. Check if any hooks match the requested pattern
        4. Run the hook's callback, collect in a single final_result
        5. If any of the hooks are denied, stop
        6. Return the final_result...
        """

        result = {}
        for hk in self._hooks[event]:
            if not _match(hk.matcher, tool_name):
                continue
            print(f"*********EXECUTING HOOK:{hk}")
            hook_input = None
            if event == HookEvent.PRE_TOOL_USE:
                hook_input = PreToolUseInput(
                    session_id="",
                    cwd=os.getcwd(),
                    hook_name=hk.name,
                    tool_name=tool_name,
                    tool_input=input_data or {},
                    tool_use_id=tool_name or "",
                )

            output = hk.run(hook_input) or HookOutput(decision=PermissionDecision.ALLOW)
            
            if output.decision == PermissionDecision.DENY:
                return {
                    hk.name: output
                }
            elif output.decision == PermissionDecision.MODIFIED:
                # TODO: what do we do
                print("ERROR: MODIFIED OUTPUTS NOT IMPLEMENTED")
                pass
            else:
                result[hk.name] = output

        return result
        

def _match(pattern: str | None, tool_name: str) -> bool:
    if pattern is None:
        return True
    return bool(re.search(pattern, tool_name))
    
