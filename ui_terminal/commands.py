import os
import sys
from typing import Callable, Any, Type, Tuple


from core.util_validators import validate_parameter
from core.exceptions import GoalError
from core.engine import goal_manager as goal_manager
from core.engine import central_registry as central_registry


command_list = {}


def command(
        categories: str | list[str],
        command: str,
        description: str,
        ):
    
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
        target_duration = input_handler("Enter target duration (seconds).", int)
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

# =====================
# Print Commands
# =====================
@command(
        command="print_central_registry",
        description="Prints the central registry which contains every object the user has made. "
        "warning: Ugly, actually prints the objects.",
        categories="main_menu",
)
def print_central_registry():
    clear_screen()
    print(f"central_registry: ")
    print(f"{central_registry.central_registry}")
    enter_to_continue()

@command(
        command="print_goal",
        description="Select and print a goal and its data.",
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
    
    print("List of goals: ")
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
        command="exit",
        description="Exits the program.",
        categories="main_menu",
)
def exit():
    sys.exit()

