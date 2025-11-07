import json
from pathlib import Path
from engine.goal_manager import UserGoal

SAVE_PATH = Path("saves/goals.json")
SAVE_PATH.parent.mkdir(exist_ok=True)