import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
from uuid import uuid4

from hooks.types import (
    Hook,
    HookEvent,
    HookOutput,
    MessageSender,
    MessageType,
    PostMessageSentInput,
    PreToolUseInput,
)
from hooks.log_message_sent import LogMessageSent
from hooks.log_tool_use import LogToolUse
from hooks.tool_permissions import ToolPermissions

HookCallback = Callable[[dict, str | None], dict]

_HOOK_REGISTRY = {
    HookEvent.PRE_TOOL_USE: [ToolPermissions, LogToolUse],
    HookEvent.POST_MESSAGE_SENT: [LogMessageSent],
}
"""
Event: Hook[]

e.g., PreToolUse: [LogToolRequest]
"""

class HookRegistry:
    def __init__(self):
        self._hooks: dict[str, list[Hook]] = _HOOK_REGISTRY
        self.session_id = _new_session_id()
        self.cwd = os.getcwd()
        self._create_session_file()

    def run(self, event: HookEvent, tool_name=None, input_data=None) -> dict[str, HookOutput]:
        """
        1. Take event, input_data, tool_use_id
        2. Get hooks registered for the event
        3. Run the hook's callback, collect in a single final_result
        4. If any hooks stop the chain, stop
        5. Return the final_result
        """

        result = {}
        for hk in self._hooks.get(event, []):
            print(f"*********EXECUTING HOOK:{hk}")
            hook_input = None
            if event == HookEvent.PRE_TOOL_USE:
                hook_input = PreToolUseInput(
                    session_id=self.session_id,
                    cwd=self.cwd,
                    hook_name=hk.name,
                    tool_name=tool_name,
                    tool_input=input_data or {},
                    tool_use_id=tool_name or "",
                )
            elif event == HookEvent.POST_MESSAGE_SENT:
                message_input = input_data or {}
                hook_input = PostMessageSentInput(
                    session_id=self.session_id,
                    cwd=self.cwd,
                    hook_name=hk.name,
                    sender=MessageSender(message_input["sender"]),
                    message_type=MessageType(message_input.get("message_type", MessageType.MESSAGE)),
                    contents=message_input.get("contents", ""),
                )

            output = hk.run(hook_input) or HookOutput()

            result[hk.name] = output
            if not output.should_continue:
                return {
                    hk.name: output
                }

        return result

    def _create_session_file(self) -> None:
        session_path = Path(self.cwd) / ".my-coding-agent" / "sessions" / f"{self.session_id}.json"
        try:
            session_path.parent.mkdir(parents=True, exist_ok=True)
            if not session_path.exists():
                session_path.write_text("[]\n")
        except Exception as exc:
            print(f"WARNING: failed to create session log: {exc}")


def _new_session_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return f"{timestamp}-{uuid4().hex[:8]}"
    
