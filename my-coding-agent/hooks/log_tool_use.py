
from hooks.types import Hook, PermissionDecision, PreToolUseInput, PreToolUseOutput

def run(input_data: PreToolUseInput):
    print(f"LOOK MOM, I'M EXECUTING THE TOOL {input_data.tool_name}")
    return PreToolUseOutput(decision=PermissionDecision.ALLOW)

LogToolUse = Hook(
    name="LogToolUse",
    matcher=None,
    timeout=30,
    run=run,
)
