

from ui_terminal.commands.commands_core import (
    command, clear_screen, input_handler, CancelCommand, time_input,
    enter_to_continue,
)
from core.engine import goal_manager as goal_manager
from core.engine import central_registry as central_registry


def display_goals() -> None:
    print("Goal list:")
    print()
    for goal_name in central_registry.central_registry["goals"]:
        print(goal_name)
        
def select_goal() -> str:
    goals = central_registry.central_registry["goals"]
    
    while True:
        selected_goal_name = input_handler("Select a goal.", str)
        if selected_goal_name not in goals:
            print("No goal with that name exists, try again.")
            continue
        return selected_goal_name


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
    
    display_goals()
    print()

    try:
        selected_goal_name = select_goal()
        selected_goal = goals[selected_goal_name]
    
        progress_seconds = time_input("Enter progress amount (Ex: 2h 33m 20s)")
        
        selected_goal.add_goal_progress(progress_seconds=progress_seconds)
    
    except CancelCommand:
        return

@command(
    command="change_description",
    description="Change a goal's description",
    categories="main_menu",
)
def change_description():
    goals = central_registry.central_registry["goals"]
    clear_screen()
    
    display_goals()
    print()
    
    try:
        selected_goal_name = select_goal()
        selected_goal = goals[selected_goal_name]
        
        print("Current description: ")
        print()
        print(f"{selected_goal.description}")
        print()
        
        new_description = input_handler("Enter new description.", str)
        selected_goal.change_description(new_description)
        
    except CancelCommand:
        return