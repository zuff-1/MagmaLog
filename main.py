

from ui_terminal import user_interface as user_interface
from core.engine import goal_manager
from core.exceptions import GoalError
import traceback

def main_sequence():
    while True:
        user_interface.main_menu()


if __name__ == "__main__":
    main_sequence()