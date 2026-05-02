from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class ToolHookContext:
    tool_name: str
    raw_args: Dict[str, Any]
    decoded_params: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    exception: Optional[Exception] = None
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: Optional[datetime] = None

    def finish(self) -> None:
        self.ended_at = datetime.now(timezone.utc)
