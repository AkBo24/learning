import json
from datetime import datetime, timezone
from pathlib import Path

from hooks.types import Hook, PostMessageSentInput, PostMessageSentOutput


def _session_path(cwd: str, session_id: str) -> Path:
    return Path(cwd) / ".my-coding-agent" / "sessions" / f"{session_id}.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run(input_data: PostMessageSentInput) -> PostMessageSentOutput:
    session_path = _session_path(input_data.cwd, input_data.session_id)

    try:
        session_path.parent.mkdir(parents=True, exist_ok=True)

        if session_path.exists():
            with open(session_path, "r") as f:
                messages = json.load(f)
            if not isinstance(messages, list):
                messages = []
        else:
            messages = []

        messages.append({
            "from": input_data.sender.value,
            "type": input_data.message_type.value,
            "contents": input_data.contents,
            "message_sent": _utc_now(),
        })

        temp_path = session_path.with_suffix(".tmp")
        with open(temp_path, "w") as f:
            json.dump(messages, f, indent=2)
            f.write("\n")
        temp_path.replace(session_path)
    except Exception as exc:
        print(f"WARNING: failed to log message: {exc}")

    return PostMessageSentOutput()


LogMessageSent = Hook(
    name="LogMessageSent",
    timeout=30,
    run=run,
)
