from dataclasses import dataclass
from typing import Callable

from hooks.types.hook_input import HookInput
from hooks.types.hook_output import HookOutput


@dataclass(frozen=True)
class Hook:
    name: str
    timeout: int
    run: Callable[[HookInput], HookOutput]
