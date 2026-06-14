import json
from pathlib import Path
from typing import Any

from hooks.types import Hook, PermissionDecision, PreToolUseInput, PreToolUseOutput


def _config_path(cwd: str) -> Path:
    return Path(cwd) / ".my-coding-agent" / "tool-use-config.json"


def _ensure_config(path: Path) -> None:
    if path.exists():
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump({}, f, indent=2)
        f.write("\n")


def _read_config(cwd: str) -> dict[str, Any]:
    config_path = _config_path(cwd)
    try:
        _ensure_config(config_path)
        with open(config_path, "r") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}

    if not isinstance(config, dict):
        return {}

    return config


def run(input_data: PreToolUseInput) -> PreToolUseOutput:
    config = _read_config(input_data.cwd)
    tools = config.get("tools", {})
    if not isinstance(tools, dict):
        return PreToolUseOutput(decision=PermissionDecision.ALLOW)

    tool_config = tools.get(input_data.tool_name, {})
    print(f"*********TOOL CONFIG: {tool_config}")
    if not isinstance(tool_config, dict):
        return PreToolUseOutput(decision=PermissionDecision.ALLOW)

    status = str(tool_config.get("status", "")).lower()
    if status == PermissionDecision.DENY.value:
        return PreToolUseOutput(
            decision=PermissionDecision.DENY,
            should_continue=False,
            denial_reason=f"Tool '{input_data.tool_name}' is disabled by tool permissions.",
        )

    return PreToolUseOutput(decision=PermissionDecision.ALLOW)


ToolPermissions = Hook(
    name="ToolPermissions",
    timeout=30,
    run=run,
)
