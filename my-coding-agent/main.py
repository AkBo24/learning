import inspect
import json
import os

from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from typing import Any, Dict, List, Tuple

load_dotenv()

client = OpenAI()

YOU_COLOR = "\u001b[94m"
ASSISTANT_COLOR = "\u001b[93m"
RESET_COLOR = "\u001b[0m"

SYSTEM_PROMPT = """
You are a coding assistant whose goal it is to help us solve coding tasks. 
You have access to a series of tools you can execute. Here are the tools you can execute:

{tool_list_repr}
"""

YOU_COLOR = "\u001b[94m"
ASSISTANT_COLOR = "\u001b[93m"
RESET_COLOR = "\u001b[0m"

# https://developers.openai.com/api/docs/guides/function-calling
# May not be the exact way we set this up. see the system prompt for how we tell the llm to 
# call tools

def resolve_abs_path(path_str: str) -> Path:
    """
    file.py -> /Users/you/project/file.py
    """
    path = Path(path_str).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return path

def read_file_tool(filename: str) -> Dict[str, Any]:
    """
    Gets the full content of a file provided by the user.
    :param filename: The name of the file to read.
    :return: The full content of the file.
    """
    full_path = resolve_abs_path(filename)
    print(full_path)
    with open(str(full_path), "r") as f:
        content = f.read()
    return {
        "file_path": str(full_path),
        "content": content
    }

READ_FILE = "read_file"
TOOL_REGISTRY = {
    READ_FILE: read_file_tool
}

tools = [
    {
        "type": "function",
        "name": READ_FILE,
        "description": "Gets the full content of a file provided by the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the file to read. ",
                },
            },
            "required": ["filename"],
        },
    },
]

def get_tool_str_representation(tool_name: str) -> str:
    tool = TOOL_REGISTRY[tool_name]
    return f"""
    Name: {tool_name}
    Description: {tool.__doc__}
    Signature: {inspect.signature(tool)}
    """

def get_full_system_prompt():
    tool_str_repr = ""
    for tool_name in TOOL_REGISTRY:
        tool_str_repr += "TOOL\n===" + get_tool_str_representation(tool_name)
        tool_str_repr += f"\n{'='*15}\n"
    return SYSTEM_PROMPT.format(tool_list_repr=tool_str_repr)

def execute_llm_call(conversation: List[Dict[str, str]]):
    system_content = ""
    messages = []

    for msg in conversation:
        if msg.get("role") == "system":
            system_content = msg["content"]
        else:
            messages.append(msg)

    response = client.responses.create(
        model="gpt-5.5",
        instructions=system_content,
        input=messages,
        tools=tools
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
    Return list of (tool_name, args) requested in 'tool: name({...})' lines.
    The parser expects single-line, compact JSON in parentheses.
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
    print("*********** SYSTEM PROMPT *************")
    print(get_full_system_prompt())
    print("*********** SYSTEM PROMPT *************")

    conversation = [{
        "role": "system",
        "content": get_full_system_prompt()
    }]

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
            assistant_output, assistant_response = execute_llm_call(conversation)
            tool_invocations = extract_tool_invocations(assistant_output)

            if not tool_invocations:
                # Assuming always a text response back to user
                output_text = assistant_response.output_text
                print(f"{ASSISTANT_COLOR}Assistant:{RESET_COLOR}: {output_text}")
                conversation.append({
                    "role": "assistant",
                    "content": output_text
                })
                break

            for name, args, _ in tool_invocations:
                tool = TOOL_REGISTRY[name]
                resp = ""
                print(name, args)

                if name == READ_FILE:
                    resp = tool(args.get("filename", "."))

                conversation.append({
                    "role": "user",
                    "content": f"tool_result({json.dumps(resp)})"
                })
    return

if __name__ == "__main__":
    run_coding_agent_loop()