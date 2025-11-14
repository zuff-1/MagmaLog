import os
import sys
from typing import Callable


from core.validators import validate_parameter
from core.engine import goal_manager as goal_manager
from core.engine import central_registry as central_registry


command_list = {}


def command(
        categories: str | list[str],
        command: str,
        description: str,
        ):
    if not isinstance(categories, (str, list)):
        raise TypeError(
            "categories must be a string or a list of strings"
            f"received: {categories}"
            f"type: {type(categories).__name__}"
        )
    if isinstance(categories, list) and not all(isinstance(list_item, str) for list_item in categories):
        items = []
        for list_item in categories:
            validity = isinstance(list_item, str)
            items.append({list_item: validity})
        raise TypeError(
            "all items in categories list must be strings\n"
            "items received and their validity :\n"
            f"{items}"
        )
    if not isinstance(command, str):
        raise TypeError(
            "command must be a string\n"
            f"received: {command}"
            f"type: {type(command).__name__}"
        )
    if not isinstance(description, str):
        raise TypeError(
            "description must be a string\n"
            f"received: {description}"
            f"type: {type(description).__name__}"
        )
    
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
            command_list[cat][command] = {"description": description, "function": func}
        return func
    return decorator

def default_handle_error(e: Exception):
    print(f"{type(e).__name__}: {e}")

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
    name = input("Enter goal name: ")
    description = input("Enter description: ")
    while True:
        target_duration = input("Enter target duration (in seconds for now): ")
        try:
            target_duration = int(target_duration)
            break
        except ValueError:
            print("Target duration must be an integer number, try again.")
    try:
        goal_manager.UserGoal(
            name=name,
            target_duration=target_duration,
            description=description
        )
    except Exception as e:
        default_handle_error(e)

# =====================
# Print Commands
# =====================
@command(
        command="print_central_registry",
        description="Prints the central registry which contains every object the user has made.",
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

    print("List of goals:")
    print()
    for goals in registry["goals"]:
        print(f"{goals}")
    print()
    print("Enter a goal name to print.")
    while True:
        user_input = input(">")
        if user_input in registry["goals"]:
            break
        else:
            print("Input is not a goal name, try again.")
    selected_goal = registry["goals"][user_input]
    goal_dict_form = selected_goal.to_dict()
    print(f"{goal_dict_form}")
    enter_to_continue()

@command(
        command="print_all_goals",
        description="Choose a goal and print every data it has it a human readable form.",
        categories="main_menu",
)
def print_all_goals():
    registry = central_registry.central_registry

    print("Goals in central_registry: ")
    for goal in registry["goals"]:
        goal_obj = registry["goals"][goal]
        goal_dict_form = goal_obj.to_dict()
        print(f"{goal_dict_form}")
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

