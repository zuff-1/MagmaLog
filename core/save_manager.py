

import json
from pathlib import Path
from platformdirs import user_data_dir


from core.engine.goal_manager import UserGoal
from core.utilities.validators import validate_parameter


APP_NAME = "MagmaLog"
APP_AUTHOR = "Z_UFF"

APP_DIR = Path(user_data_dir(APP_NAME))
SAVE_DIR = APP_DIR / "saves"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

selected_save_name = None

def get_selected_save_name():
    return selected_save_name

def get_profile_path(name: str) -> Path:
    validate_parameter(name, "name", str)
    return SAVE_DIR / f"{name}.json"

def list_profile_names():
    return [p.stem for p in SAVE_DIR.glob("*.json")]

def select_profile(name: str):
    validate_parameter(name, "name", str)
    profiles = list_profile_names()

    if name not in profiles:
        raise ValueError(
            "profile doesn't exist, cannot be selected.\n"
            f"received: {name}\n"
            f"profiles: {profiles}"
        )
    
    global selected_save_name
    selected_save_name = name

def create_profile(name: str):
    validate_parameter(name, "name", str)
    path = get_profile_path(name)

    if path.exists():
        raise ValueError(f"Profile already exists! : {name}")

    data = {}

    path.write_text(json.dumps(data, indent=4))

def save_data(name: str, registry: dict) -> None:
    validate_parameter(name, "name", str)
    validate_parameter(registry, "registry", dict)
    SAVE_PATH = get_profile_path(name)
    
    serializable = {
        "goals": {
            name: goal.to_dict()
            for name, goal in registry["goals"].items()
        }
    }
    
    with SAVE_PATH.open("w", encoding="utf-8") as handle:
        json.dump(serializable, handle, indent=4)
        
def load_data(name: str):
    validate_parameter(name, "name", str)
    SAVE_PATH = get_profile_path(name)
    
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