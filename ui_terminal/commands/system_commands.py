import sys


from ui_terminal.commands.commands_core import (
    command, enter_to_continue, input_handler, CancelCommand, clear_screen,
    are_you_sure
)
from core.engine import goal_manager as goal_manager
from core.engine import central_registry as central_registry
from core import save_manager


@command(
    command="create_profile",
    description="Create a profile.",
    categories=["main_menu", "start_menu"],
)
def create_profile():
    clear_screen()
    profiles = save_manager.list_profile_names()
    while True:
        try:
            user_input = input_handler("Enter profile name.", str)
        except CancelCommand:
            return
        if user_input in profiles:
            print("A profile with that name already exists, make a new name.")
            continue
        break
    save_manager.create_profile(user_input)

@command(
    command="select_profile",
    description="Select a profile to load and switch into.",
    categories=["main_menu", "start_menu"],
)
def select_profile():
    clear_screen()
    profiles = save_manager.list_profile_names()
    
    if not profiles:
        print("There is no save file to select.")
        enter_to_continue()
        return
    
    print("Profiles list: ")
    print()
    for profile in profiles:
        print(profile)
    print()
    while True:
        try:
            selected_profile = input_handler("Enter a profile name to select.", str)
        except CancelCommand:
            return
        if selected_profile not in profiles:
            print("No profile with that name exists, try again.")
            continue
        break
        
    current_selected_profile = save_manager.get_selected_save_name()
    if current_selected_profile:
        save_manager.save_data(current_selected_profile, central_registry.central_registry)
        
    save_manager.select_profile(selected_profile)
    central_registry.central_registry = central_registry.get_template_registry()
    central_registry.central_registry = save_manager.load_data(selected_profile)



@command(
    command="save_data",
    description="Saves your data into the current selected profile.",
    categories=["main_menu"],
)
def save_data():
    clear_screen()
    registry = central_registry.central_registry
    save = save_manager.get_selected_save_name()
    
    if not save:
        print("No profile is currently selected, save cancelled")
        enter_to_continue()
        return
        
    save_manager.save_data(save, registry)

@command(
    command="save_data_as",
    description="Save data into a selected profile.",
    categories=["main_menu"],
)
def save_data_as():
    clear_screen()
    profiles = save_manager.list_profile_names()
    registry = central_registry.central_registry
    
    if not profiles:
        print("There is no save file to select.")
        enter_to_continue()
        return
    
    print("Profiles list: ")
    print()
    for profile in profiles:
        print(profile)
        print()
    while True:
        try:
            selected_profile = input_handler("Enter a profile name to save into.", str)
        except CancelCommand:
            return
        if selected_profile not in profiles:
            print("No profile with that name exists, try again.")
            continue
        break
    try:
        are_you_sure()
    except CancelCommand:
        return
    
    save_manager.save_data(selected_profile, registry)

@command(
        command="exit",
        description="Exits the program.",
        categories=["main_menu", "start_menu"],
)
def exit():
    sys.exit()    








def load_data():
    """
    Unused command, loads data without switching profiles.
    dangerous and unintuitive to the user.
    """
    clear_screen()
    profiles = save_manager.list_profile_names()
    
    if not profiles:
        print("There is no save file to load.")
        enter_to_continue()
        return
    
    print("Profiles list: ")
    print()
    for profile in profiles:
        print(profile)
        print()
    while True:
        try:
            selected_profile = input_handler("Enter a profile name to load.", str)
            if selected_profile not in profiles:
                print("No profile with that name exists, try again.")
                continue
        except CancelCommand:
            return
        break
    
    save_manager.load_data(selected_profile)
            
