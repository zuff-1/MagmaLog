import os
import sys
from typing import Callable, Any, Type
import re


from core.utilities.validators import validate_parameter
from core.engine import goal_manager as goal_manager
from core.engine import central_registry as central_registry
from core import save_manager


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
        raise ValueError(f"Invalid time format, no matches found: {input}")
    
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


def default_handle_error(e: Exception):
    print(f"{type(e).__name__}: {e}")
    enter_to_continue()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def enter_to_continue():
    input("Press Enter to continue. . .")
    

# =====================
# Goal Commands
# =====================
@command(
        command="create_goal",
        description="Creates a new goal.",
        categories="main_menu",
        )
def create_goal():
    clear_screen()
    registry = central_registry.central_registry
    goals = registry["goals"]
    try:
        
        while True:
            try:
                name = input_handler("Enter goal name.", str)
            except CancelCommand:
                return
            if name in goals:
                print("A goal with that name already exists, try again.")
                continue
            break
        
        target_duration = time_input("Enter target duration. (Ex: 4h 47m 27s)")
        
        description = input_handler(
            prompt="Enter description (can be empty)",
            expected_type=str,
            allow_empty=True,
            default_value="No description",
        )
        
        goal_manager.UserGoal(
            name=name,
            target_duration=target_duration,
            description=description,
        )
        
    except CancelCommand:
        return

@command(
    command="add_goal_progress",
    description="Log your progress on a goal.",
    categories="main_menu",
)
def add_goal_progress():
    clear_screen()
    registry = central_registry.central_registry
    goals = registry["goals"]
    
    if not goals:
        print("There is no goal to log progress into, create a goal first.")
        enter_to_continue()
        return
    
    print("Goal list:")
    print()
    for goal_name in goals:
        print(goal_name)
    print() 

    try:
        while True:
            try:
                selected_goal_name = input_handler("Select a goal.", str)
            except CancelCommand:
                return
            if selected_goal_name not in goals:
                print("No goal with that name exists, try again.")
                continue
            selected_goal = goals[selected_goal_name]
            break
        
        progress_seconds = time_input("Enter progress amount (Ex: 2h 33m 20s)")
        
        selected_goal.add_goal_progress(progress_seconds=progress_seconds)
    
    except CancelCommand:
        return

# =====================
# Print Commands
# =====================
@command(
        command="print_central_registry",
        description="Prints the central registry which contains every object the user has made. "
        "warning: Not human readable.",
        categories="main_menu",
)
def print_central_registry():
    clear_screen()
    print(f"central_registry: ")
    print(f"{central_registry.central_registry}")
    enter_to_continue()

@command(
        command="print_goal",
        description="Select and print a goal's properties. (long progress data excluded)",
        categories="main_menu",
)
def print_goal():
    clear_screen()
    registry = central_registry.central_registry
    goals = registry["goals"]

    if not goals:
        print("There are no goals to print.")
        enter_to_continue()
        return
    
    print("Goal list: ")
    print()
    for goal_name in goals:
        print(goal_name)
    print()

    while True:
        try:
            selected_name = input_handler(
                prompt="Input a goal name to print.",
                expected_type=str,
            )
        except CancelCommand:
            return
        if selected_name not in goals:
            print("No goal with that name exists, try again.")
            continue
        break
    
    goal = goals[selected_name]
    goal_data = goal.to_dict()
    
    clear_screen()
    print(f"Goal : {selected_name}")
    print()
    for key, value in goal_data.items():
        if key == "target_duration":
            value = format_time_int(value)
        if key == "data":
            continue
        print(f"{key}: {value}")
    print()
    enter_to_continue()

@command(
        command="print_all_goals",
        description="Choose a goal and print every data it has it a human readable form.",
        categories="main_menu",
)
def print_all_goals():
    clear_screen()
    registry = central_registry.central_registry
    goals = registry["goals"]

    if not goals:
        print("There are no goals to print.")
        enter_to_continue()
        return
    
    for goal_name in goals:
        goal_obj = goals[goal_name]
        goal_data = goal_obj.to_dict()
        
        print(f"Goal : {goal_name}")
        print()
        for key, value in goal_data.items():
            print(f"{key}: {value}")
        print()
    enter_to_continue()

# =====================
# Utility Commands
# =====================

@command(
    command="save_data",
    description="saves your data.",
    categories="main_menu",
)
def save_data():
    registry = central_registry.central_registry
    save_manager.save_data(registry)

@command(
    command="load_data",
    description="loads your save file.",
    categories="main_menu"
)
def load_data():
    save_manager.load_data()

@command(
        command="exit",
        description="Exits the program.",
        categories="main_menu",
)
def exit():
    sys.exit()

