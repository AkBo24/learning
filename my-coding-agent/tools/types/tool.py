from dataclasses import dataclass
from typing import Any, Callable, Dict

from tools.types.tool_names import ToolName


@dataclass(frozen=True)
class Tool:
    name: ToolName
    description: str
    parameters: Dict[str, Any]
    exec: Callable[..., Dict[str, Any]]
    decode_params: Callable[[Dict[str, Any]], Dict[str, Any]]

    def config(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "name": self.name.value,
            "description": self.description,
            "parameters": self.parameters,
        }
