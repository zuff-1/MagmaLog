import os
from typing import Callable, Any, Type
import re


from core.utilities.validators import validate_parameter
from core.engine import goal_manager as goal_manager
from core.engine import central_registry as central_registry


command_list = {}


def command(
        categories: str | list[str],
        command: str,
        description: str,
        ):
    """Put a function into command list to be used by the user in CLI.
    
    Can easily be used as a decorator, doesn't modify passed function at all.
    
    Args:
        categories (str | list[str]): Which menu the command is available in. Examples:
        - "main_menu"
        - "goal_menu"
        command (str): What the user has to input to execute the function.
        description (str): Information about the command that is displayed.

    Raises:
        KeyError: command already exists in the category.

    Returns:
        Passed function
    """
    
    validate_parameter(categories, "categories", (str, list), element_type=str)
    validate_parameter(command, "command", str)
    validate_parameter(description, "description", str)

    if isinstance(categories, str):
        categories = [categories]

    def decorator(func: Callable):
        for cat in categories:
            
            if cat not in command_list:
                command_list[cat] = {}

            if command in command_list[cat]:
                raise KeyError(
                    "command already exists in the category"
                    f"command: {command}"
                )
            command_list[cat][command] = {
                "description": description,
                "function": func
            }
        return func
    return decorator


class CancelCommand(Exception):
    """
    Raised when user inputs the cancel command.
    """
def input_handler(
        prompt: str,
        expected_type: Type,
        allow_empty: bool = False,
        default_value: Any = None,
    ):
    validate_parameter(prompt, "prompt", str)
    validate_parameter(expected_type, "expected_type", type)
    if not isinstance(allow_empty, bool):
        raise TypeError(
            "allow_empty has to be a boolean\n"
            f"received: {allow_empty}\n"
            f"type: {type(allow_empty).__name__}"
        )

    while True:
        print(prompt)
        print("(type cancel to exit command)")
        value = input(">")

        if value == "cancel":
            raise CancelCommand()
        
        if (
            not value
            and allow_empty
            and default_value is not None
            ):
            return default_value
        
        if not value and not allow_empty:
            print("Input cannot be empty, try again.\n")
            continue

        if expected_type is int:
            try:
                value = int(value)
                return value
            except ValueError:
                print("Input must be an integer number, try again.\n")
                continue

        return value
    

def parse_time_string(time_string: str) -> int:
    """Parse string of time like 5h 3m 22s into total seconds."""
    pattern = r"(\d+)\s*(h|m|s)"
    matches = re.findall(pattern, time_string.lower())
    
    if not matches:
        raise ValueError(f"Invalid time format, no matches found: {time_string}")
    
    total_seconds = 0
    
    for value, unit in matches:
        value = int(value)
        if unit == "h":
            total_seconds += value * 3600
        elif unit == "m":
            total_seconds += value * 60
        elif unit == "s":
            total_seconds += value
        else:
            raise ValueError(f"Invalid time unit: {unit}")
    
    return total_seconds


def format_time_int(total_seconds: int) -> str:
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds or not parts:
        parts.append(f"{seconds}s")
    formatted_time = " ".join(parts)
    
    return formatted_time


def time_input(prompt: str) -> int:
    validate_parameter(prompt, "prompt", str)
    
    while True:
        try:
            user_input = input_handler(prompt, str)
            total_seconds = parse_time_string(user_input)
        except ValueError as e:
            print(e)
            print("try again.")
            continue
        break
    
    return total_seconds

def are_you_sure(
    prompt: str = "Are you sure? y/n"
    ):
    validate_parameter(prompt, "prompt", str)
    while True:
        user_input = input_handler(prompt=prompt, expected_type=str)
        if user_input in ("y", "yes"):
            break
        elif user_input in ("n", "no"):
            raise CancelCommand()
        else:
            print("Enter y or n, try again.")
            continue


def default_handle_error(e: Exception):
    print(f"{type(e).__name__}: {e}")
    enter_to_continue()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def enter_to_continue():
    input("Press Enter to continue. . .")