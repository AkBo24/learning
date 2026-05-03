import subprocess
from typing import Any, Dict

from tools.enum.tool_names import ToolName
from tools.types import Tool
from tools.utils import resolve_abs_path


DESCRIPTION = "Runs a shell command from the given working directory and returns its output."

PARAMETERS = {
    "type": "object",
    "properties": {
        "command": {
            "type": "string",
            "description": "The shell command to run.",
        },
        "cwd": {
            "type": "string",
            "description": "The working directory for the command. Defaults to the current directory.",
        },
        "timeout_seconds": {
            "type": "integer",
            "description": "Maximum time to allow the command to run, from 1 to 120 seconds. Defaults to 30.",
        },
    },
    "required": ["command"],
}


def exec_tool(
    command: str,
    cwd: str = ".",
    timeout_seconds: int = 30,
) -> Dict[str, Any]:
    """
    Runs a shell command from the given working directory.
    :param command: The shell command to run.
    :param cwd: The working directory for the command.
    :param timeout_seconds: Maximum time to allow the command to run.
    :return: A dictionary with the command result.
    """
    full_cwd = resolve_abs_path(cwd)
    bounded_timeout = max(1, min(timeout_seconds, 120))

    try:
        completed = subprocess.run(
            command,
            shell=True,
            cwd=str(full_cwd),
            capture_output=True,
            text=True,
            timeout=bounded_timeout,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "cwd": str(full_cwd),
            "exit_code": None,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "timed_out": True,
            "timeout_seconds": bounded_timeout,
        }

    return {
        "command": command,
        "cwd": str(full_cwd),
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "timed_out": False,
        "timeout_seconds": bounded_timeout,
    }


def decode_params(args: Dict[str, Any]) -> Dict[str, Any]:
    try:
        timeout_seconds = int(args.get("timeout_seconds", 30))
    except (TypeError, ValueError):
        timeout_seconds = 30

    return {
        "command": args.get("command", ""),
        "cwd": args.get("cwd", "."),
        "timeout_seconds": timeout_seconds,
    }


TOOL = Tool(
    name=ToolName.RUN_SHELL_COMMAND,
    description=DESCRIPTION,
    parameters=PARAMETERS,
    exec=exec_tool,
    decode_params=decode_params,
)
