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

def list_files_tool(path: str) -> Dict[str, Any]:
    """
    Lists the files in a directory provided by the user.
    :param path: The path to a directory to list files from.
    :return: A list of files in the directory.
    """
    full_path = resolve_abs_path(path)
    all_files = []
    for item in full_path.iterdir():
        all_files.append({
            "filename": item.name,
            "type": "file" if item.is_file() else "dir"
        })
    return {
        "path": str(full_path),
        "files": all_files
    }

def edit_file_tool(path: str, old_str: str, new_str: str) -> Dict[str, Any]:
    """
    Replaces first occurrence of old_str with new_str in file. If old_str is empty,
    create/overwrite file with new_str.
    :param path: The path to the file to edit.
    :param old_str: The string to replace.
    :param new_str: The string to replace with.
    :return: A dictionary with the path to the file and the action taken.
    """
    full_path = resolve_abs_path(path)
    if old_str == "":
        full_path.write_text(new_str, encoding="utf-8")
        return {
            "path": str(full_path),
            "action": "created_file"
        }
    original = full_path.read_text(encoding="utf-8")
    if original.find(old_str) == -1:
        return {
            "path": str(full_path),
            "action": "old_str not found"
        }
    edited = original.replace(old_str, new_str, 1)
    full_path.write_text(edited, encoding="utf-8")
    return {
        "path": str(full_path),
        "action": "edited"
    }

READ_FILE = "read_file"
LIST_FILES = "list_files"
EDIT_FILE = "edit_file"
TOOL_REGISTRY = {
    READ_FILE: read_file_tool,
    LIST_FILES: list_files_tool,
    EDIT_FILE: edit_file_tool
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
                    "description": "The name of the file to read.",
                },
            },
            "required": ["filename"],
        },
    },
    {
        "type": "function",
        "name": LIST_FILES,
        "description": "Lists the files in a directory provided by the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to a directory to list files from.",
                },
            },
            "required": ["path"],
        },
    },
    {
        "type": "function",
        "name": EDIT_FILE,
        "description": "Replaces first occurrence of old_str with new_str in file. If old_str is empty, create/overwrite file with new_str.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to a directory to list files from.",
                },
                "old_str": {
                    "type": "string",
                    "description": "The string to replace.",
                },
                "new_str": {
                    "type": "string",
                    "description": "The string to replace with.",
                },
            },
            "required": ["path", "old_str", "new_str"],
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

def execute_llm_call(system_content: str, input_messages: List[Any]):
    response = client.responses.create(
        model="gpt-5.5",
        instructions=system_content,
        input=input_messages,
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
                tool = TOOL_REGISTRY[name]
                resp = ""
                print(name, args)

                if name == READ_FILE:
                    resp = tool(args.get("filename", "."))
                elif name == LIST_FILES:
                    resp = tool(args.get("path", "."))
                elif name == EDIT_FILE:
                    resp = tool(args.get("path", "."), 
                                args.get("old_str", ""), 
                                args.get("new_str", ""))

                conversation.append({
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(resp)
                })
    return

if __name__ == "__main__":
    run_coding_agent_loop()
