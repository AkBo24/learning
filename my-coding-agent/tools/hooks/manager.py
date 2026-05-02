from collections import defaultdict
from typing import Callable, DefaultDict, List

from tools.hooks.context import ToolHookContext


HookHandler = Callable[[ToolHookContext], None]

_HOOKS: DefaultDict[str, List[HookHandler]] = defaultdict(list)


def register_hook(event_name: str, handler: HookHandler) -> None:
    _HOOKS[event_name].append(handler)


def emit_hook(event_name: str, context: ToolHookContext) -> None:
    for handler in _HOOKS[event_name]:
        try:
            handler(context)
        except Exception:
            pass
