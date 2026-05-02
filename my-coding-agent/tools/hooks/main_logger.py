from pathlib import Path

from tools.hooks.context import ToolHookContext
from tools.hooks.log_format import format_tool_log_entry


LOG_FILE_PATH = Path("output") / "main.log"


def log_tool_call(context: ToolHookContext) -> None:
    log_path = Path.cwd() / LOG_FILE_PATH
    log_path.parent.mkdir(parents=True, exist_ok=True)

    status = "Tool error" if context.error is not None else "Tool success"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(format_tool_log_entry(context, status))
