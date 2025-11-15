

from ui_terminal.commands import command_list, clear_screen


def main_menu():
    category = "main_menu"
    clear_screen()

    print("====== Main Menu ======")
    print()
    print("Available commands: ")
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