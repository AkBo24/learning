import json

from openai import OpenAI
from dotenv import load_dotenv
from typing import Any, List

from tools import OPENAI_TOOLS, execute_tool
from hooks import (
    HookRegistry,
    HookEvent,
    MessageSender,
    MessageType,
    PermissionDecision,
    PreToolUseOutput,
)

load_dotenv()

client = OpenAI()
hook_registry = HookRegistry()

YOU_COLOR = "\u001b[94m"
ASSISTANT_COLOR = "\u001b[93m"
RESET_COLOR = "\u001b[0m"

SYSTEM_PROMPT = """
You are a coding assistant whose goal it is to help us solve coding tasks. 
You have access to a series of tools you can execute.
"""

YOU_COLOR = "\u001b[94m"
ASSISTANT_COLOR = "\u001b[93m"
RESET_COLOR = "\u001b[0m"

def get_full_system_prompt():
    return SYSTEM_PROMPT

def execute_llm_call(system_content: str, input_messages: List[Any]):
    response = client.responses.create(
        model="gpt-5.5",
        instructions=system_content,
        input=input_messages,
        tools=OPENAI_TOOLS
    )
    # print("*********** OUTPUT *************")
    # print(response.output)
    # print("*********** OUTPUT *************\n")

    # print("*********** FULL RESPONSE *************")
    # print(response.model_dump_json(indent=2))
    # print("*********** FULL RESPONSE *************")

    return response.output, response

def extract_tool_invocations(output):
    """
    Return list of (tool_name, args, tool_call) requested by Responses API
    function_call output items.
    """

    invocations = []

    for op in output:
        if op.type == 'function_call':

            try:
                invocation = (
                    op.name,
                    json.loads(op.arguments),
                    op
                )

                invocations.append(invocation)
            except:
                print("*********** FAILED TO LOAD TOOL CALL *************")
                print(op)
                print("*********** FAILED TO LOAD TOOL CALL *************")

    return invocations


def log_message_sent(sender: MessageSender, contents: str):
    hook_registry.run(
        HookEvent.POST_MESSAGE_SENT,
        hook_payload={
            "sender": sender,
            "message_type": MessageType.MESSAGE,
            "contents": contents,
        },
    )

def run_coding_agent_loop():
    system_content = get_full_system_prompt()

    print("*********** SYSTEM PROMPT *************")
    print(system_content)
    print("*********** SYSTEM PROMPT *************")
    log_message_sent(MessageSender.SYSTEM, system_content)

    conversation: List[Any] = []

    while True:
        try:
            user_input = input(f"{YOU_COLOR}You:{RESET_COLOR}:")
        except (KeyboardInterrupt, EOFError):
            break

        user_message = user_input.strip()
        conversation.append({
            "role": "user",
            "content": user_message
        })
        log_message_sent(MessageSender.USER, user_message)

        while True:
            assistant_output, assistant_response = execute_llm_call(system_content, conversation)
            tool_invocations = extract_tool_invocations(assistant_output)

            if not tool_invocations:
                # Assuming always a text response back to user
                output_text = assistant_response.output_text
                print(f"{ASSISTANT_COLOR}Assistant:{RESET_COLOR}: {output_text}")
                conversation.extend(assistant_output)
                log_message_sent(MessageSender.AGENT, output_text)
                break

            conversation.extend(assistant_output)

            for name, args, tool_call in tool_invocations:
                print(name, args)
                hook_output = hook_registry.run(
                    HookEvent.PRE_TOOL_USE,
                    hook_payload=args,
                    metadata={
                        "tool_name": name,
                    }
                )

                denied_output = next(
                    (
                        ho
                        for ho in hook_output.values()
                        if isinstance(ho, PreToolUseOutput)
                        and ho.decision == PermissionDecision.DENY
                    ),
                    None,
                )
                if denied_output is not None:
                    resp = {
                        "error": "Tool use denied",
                        "tool_name": name,
                        "reason": denied_output.denial_reason or "Tool use was denied by a hook.",
                    }
                else:
                    resp = execute_tool(name, args)

                conversation.append({
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(resp)
                })
    return

if __name__ == "__main__":
    run_coding_agent_loop()
