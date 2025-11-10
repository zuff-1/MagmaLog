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
        raise TypeError(f"key must be a string or list of strings, received: {type(key).__name__}")
    
    if isinstance(key, list) and not all(isinstance(list_item, str) for list_item in key):
        items = []
        for list_item in key:
            items.append
        raise TypeError(
            "all items in key list must be strings"
            "items receieved : {}"
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
    if not isinstance(key, (str, list)):
        raise TypeError(f"key must be a string or list of strings, receieved: {type(key).__name__}")
    
    if isinstance(key, list) and not all(isinstance(list_item, str) for list_item in key):
        raise TypeError("all items in key list must be strings.")
    
    
    ref = central_registry

    if isinstance(key, str):
        return ref[key]
    else:
        for i in key:
            ref = ref[i]
        return ref


if __name__ == "__main__":
    pass