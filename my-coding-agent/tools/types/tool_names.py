from enum import Enum


class ToolName(str, Enum):
    READ_FILE = "read_file"
    LIST_FILES = "list_files"
    EDIT_FILE = "edit_file"
    DELETE_FILE = "delete_file"
    RUN_SHELL_COMMAND = "run_shell_command"
