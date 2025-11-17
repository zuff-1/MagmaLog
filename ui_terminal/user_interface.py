

from ui_terminal.commands.commands_core import (
    command_list, clear_screen
)
from core import save_manager


def main_menu():
    category = "main_menu"
    save_name = save_manager.get_selected_save_name
    clear_screen()

    print("============ Main Menu ============")
    print(f"Save file: {save_name()}")
    print()
    print("Available commands: ")
    print("Scroll up if you can't see save file info lol")
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