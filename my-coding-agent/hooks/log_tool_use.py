
from hooks.types import Hook, PreToolUseInput, HookOutput, PermissionDecision

def run(input_data: PreToolUseInput):
    print(f"LOOK MOM, I'M EXECUTING THE TOOL {input_data.tool_name}")
    return HookOutput(decision=PermissionDecision.ALLOW)

LogToolUse = Hook(
    name="LogToolUse",
    matcher=None,
    timeout=30,
    run=run,
)
