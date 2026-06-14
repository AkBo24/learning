from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict


class MessageSender(str, Enum):
    USER = "USER"
    AGENT = "AGENT"
    SYSTEM = "SYSTEM"


class MessageType(str, Enum):
    MESSAGE = "MESSAGE"


@dataclass(frozen=True)
class HookInput:
    session_id: str
    cwd: str
    hook_name: str

@dataclass(frozen=True)
class PreToolUseInput(HookInput):
    tool_name: str
    tool_input: Dict[str, Any]
    tool_use_id: str


@dataclass(frozen=True)
class PostMessageSentInput(HookInput):
    sender: MessageSender
    message_type: MessageType
    contents: str
