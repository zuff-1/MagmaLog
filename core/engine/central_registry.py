# reminders from nighttime:
#-unfinished raise and stuff in goal_manager
#-minutes and hours conversion should not be handled inside of goal_manager's core functions.
# thats about it really,
# to be added:
#-scan and cleanup through every single file,
#adding annotations, error raises, type handling, etc.
# please sleep better next time, 4 hours was bad.

from typing import Any


central_registry = {
    "goals": {},
}


def set_central_registry(key: str | list[str], obj: Any):
    if not key:
        raise ValueError(
            "Key cannot be empty"
            "edge case, the key is most likely an empty list/anything falsy."
        )

    if not isinstance(key, (str, list)):
        raise TypeError(
                        f"key must be a string or list containing strings."
                        f"received: {type(key).__name__}"
                    )
    
    if isinstance(key, list) and not all(isinstance(list_item, str) for list_item in key):
        items = []
        for list_item in key:
            validity = isinstance(list_item, str)
            items.append({list_item: validity})
        raise TypeError(
            f"all items in key list must be strings\n"
            f"items received and their validity : \n"
            f"{items}"
        )

    if isinstance(key, str):
        central_registry[key] = obj
        return
    else:
        ref = central_registry
        for i in key[:-1]:
            if i not in ref:
                ref[i] = {}
            ref = ref[i]
        ref[key[-1]] = obj

def get_central_registry(key: str | list[str]):
    if not key:
        raise ValueError(
            "Key cannot be empty"
            "edge case, the key is most likely an empty list/anything falsy."
        )

    if not isinstance(key, (str, list)):
        raise TypeError(
                        f"key must be a string or list containing strings."
                        f"received: {type(key).__name__}"
                    )
    
    if isinstance(key, list) and not all(isinstance(list_item, str) for list_item in key):
        items = []
        for list_item in key:
            validity = isinstance(list_item, str)
            items.append({list_item: validity})
        raise TypeError(
            f"all items in key list must be strings\n"
            f"items received and their validity : \n"
            f"{items}"
        )
    
    ref = central_registry

    if isinstance(key, str):
        return ref[key]
    else:
        for i in key:
            ref = ref[i]
        return ref


if __name__ == "__main__":
    pass