import datetime
import time


from core.utilities import validators
from ui_terminal.commands.commands_core import (
    command_list, clear_screen, command
)
from core import save_manager

# Utils ===================================================

def display_and_input_commands(category: str):
    validators.validate_parameter(category, "category", str)

    print("Commands:")
    print()
    for cmd in command_list[category]:
        print(f"{cmd} : {command_list[category][cmd]["description"]}")
    while True:
        user_input = input(">")
        if user_input in command_list[category]:
            command_list[category][user_input]["function"]()
            break
        else:
            print("Invalid command, try again.")

# Menu Commands ===================================================

@command(
        command="cd_main_menu",
        description="go to main_menu",
        categories="start_menu",
)
def cd_main_menu():
    main_menu()
    
@command(
        command="cd_goal_menu",
        description="Go to the goal menu where all goal control is.",
        categories="main_menu"
)
def cd_goal_menu():
    goal_menu()

# Menus ===================================================

def main_menu():
    clear_screen()
    category = "main_menu"
    save_name = save_manager.get_selected_save_name

    print("============ Main Menu ============")
    print(f"Save file: {save_name()}")
    print()
    display_and_input_commands(category)


def start_menu():
    clear_screen()
    category = "start_menu"
    save_name = save_manager.get_selected_save_name

    print("============ Start Menu ============")
    print(datetime.date.today())
    print(f"Selected profile: {save_name()}")
    print()
    display_and_input_commands(category)

def goal_menu():
    clear_screen()
    category = "goal_menu"
    save_name = save_manager.get_selected_save_name

    print("============ Goal Menu ============")
    print(f"Selected profile: {save_name()}")
    print()
    display_and_input_commands(category)
