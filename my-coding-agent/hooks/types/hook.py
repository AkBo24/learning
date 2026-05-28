from dataclasses import dataclass
from typing import Callable, Optional

from hooks.types.hook_input import HookInput
from hooks.types.hook_output import HookOutput


@dataclass(frozen=True)
class Hook:
    name: str
    matcher: Optional[str]
    timeout: int
    run: Callable[[HookInput], HookOutput]
