import json
from pathlib import Path
from core.engine.goal_manager import UserGoal

BASE_DIR = Path(__file__).parent
SAVE_DIR = BASE_DIR / "saves"
SAVE_DIR.mkdir(exist_ok=True)

SAVE_PATH = SAVE_DIR / "save1.json"