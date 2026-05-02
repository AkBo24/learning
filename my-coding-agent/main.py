import inspect
import json

from openai import OpenAI
from dotenv import load_dotenv
from typing import Any, List

from tools import OPENAI_TOOLS, TOOL_REGISTRY, execute_tool

load_dotenv()

client = OpenAI()

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

def run_coding_agent_loop():
    system_content = get_full_system_prompt()

    print("*********** SYSTEM PROMPT *************")
    print(system_content)
    print("*********** SYSTEM PROMPT *************")

    conversation: List[Any] = []

    while True:
        try:
            user_input = input(f"{YOU_COLOR}You:{RESET_COLOR}:")
        except (KeyboardInterrupt, EOFError):
            break

        conversation.append({
            "role": "user",
            "content": user_input.strip()
        })

        while True:
            assistant_output, assistant_response = execute_llm_call(system_content, conversation)
            tool_invocations = extract_tool_invocations(assistant_output)

            if not tool_invocations:
                # Assuming always a text response back to user
                output_text = assistant_response.output_text
                print(f"{ASSISTANT_COLOR}Assistant:{RESET_COLOR}: {output_text}")
                conversation.extend(assistant_output)
                break

            conversation.extend(assistant_output)

            for name, args, tool_call in tool_invocations:
                print(name, args)
                resp = execute_tool(name, args)

                conversation.append({
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(resp)
                })
    return

if __name__ == "__main__":
    run_coding_agent_loop()
