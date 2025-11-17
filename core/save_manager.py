

import json
from pathlib import Path
from platformdirs import user_data_dir


from core.engine.goal_manager import UserGoal


APP_NAME = "MagmaLog"
APP_AUTHOR = "Z_UFF"

APP_DIR = Path(user_data_dir(APP_NAME))
SAVE_DIR = APP_DIR / "saves"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

SAVE_PATH = SAVE_DIR / "save1.json"

def save_data(registry):
    serializable = {
        "goals": {
            name: goal.to_dict()
            for name, goal in registry["goals"].items()
        }
    }
    
    with SAVE_PATH.open("w", encoding="utf-8") as handle:
        json.dump(serializable, handle, indent=4)
        
def load_data():
    if not SAVE_PATH.exists():
        input("There is no save available, press Enter to continue. . .")
        return
    
    with SAVE_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
        
    registry = {}
    
    for key, value in data.items():
        if key == "goals":
            registry["goals"] = {
                name: UserGoal.from_dict(data)
                for name, data in value.items()
            }
        else:
            registry[key] = value
    
    return registry