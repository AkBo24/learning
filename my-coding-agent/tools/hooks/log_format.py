from tools.hooks.context import ToolHookContext


def format_timestamp(context: ToolHookContext) -> str:
    ended_at = context.ended_at or context.started_at
    return ended_at.isoformat()


def format_tool_log_entry(context: ToolHookContext, title: str) -> str:
    lines = [
        f"[{format_timestamp(context)}] {title}",
        f"Tool: {context.tool_name}",
        f"Args: {context.raw_args}",
    ]

    if context.decoded_params is not None:
        lines.append(f"Decoded params: {context.decoded_params}")

    if context.result is not None:
        lines.append(f"Result: {context.result}")

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
