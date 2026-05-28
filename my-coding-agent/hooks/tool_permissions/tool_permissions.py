import json
from pathlib import Path
from typing import Any

from hooks.types import Hook, HookOutput, PermissionDecision, PreToolUseInput


CONFIG_PATH = Path(__file__).with_name("tool_permissions.json")


def _read_config() -> dict[str, Any]:
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}

    if not isinstance(config, dict):
        return {}

    return config


def run(input_data: PreToolUseInput) -> HookOutput:
    config = _read_config()
    tools = config.get("tools", {})
    if not isinstance(tools, dict):
        return HookOutput(decision=PermissionDecision.ALLOW)

    tool_config = tools.get(input_data.tool_name, {})
    print(f"*********TOOL CONFIG: {tool_config}")
    if not isinstance(tool_config, dict):
        return HookOutput(decision=PermissionDecision.ALLOW)

    status = tool_config.get("status")
    if status == PermissionDecision.DENY.value:
        return HookOutput(
            decision=PermissionDecision.DENY,
            should_continue=False,
            denial_reason=f"Tool '{input_data.tool_name}' is disabled by tool permissions.",
        )

    return HookOutput(decision=PermissionDecision.ALLOW)


ToolPermissions = Hook(
    name="ToolPermissions",
    matcher=None,
    timeout=30,
    run=run,
)
