

from ui_terminal.commands.commands_core import (
    command, clear_screen, input_handler, CancelCommand,
    enter_to_continue, format_time_int,
)
from core.engine import goal_manager as goal_manager
from core.engine import central_registry as central_registry


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
