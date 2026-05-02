from pathlib import Path

from tools.hooks.context import ToolHookContext


LOG_FILE_PATH = Path("output") / "error.log"


def _format_timestamp(context: ToolHookContext) -> str:
    ended_at = context.ended_at or context.started_at
    return ended_at.isoformat()


def _format_entry(context: ToolHookContext) -> str:
    lines = [
        f"[{_format_timestamp(context)}] Tool error",
        f"Tool: {context.tool_name}",
        f"Args: {context.raw_args}",
    ]

    if context.decoded_params is not None:
        lines.append(f"Decoded params: {context.decoded_params}")

    if context.error is not None:
        lines.append(f"Error: {context.error.get('error')}")

        exception_type = context.error.get("exception_type")
        if exception_type:
            lines.append(f"Exception type: {exception_type}")

        message = context.error.get("message")
        if message:
            lines.append(f"Message: {message}")

    if context.exception is not None and context.error is None:
        lines.append(f"Exception type: {type(context.exception).__name__}")
        lines.append(f"Message: {context.exception}")

    return "\n".join(lines) + "\n\n"


def log_tool_error(context: ToolHookContext) -> None:
    log_path = Path.cwd() / LOG_FILE_PATH
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(_format_entry(context))
