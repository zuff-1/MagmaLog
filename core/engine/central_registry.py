

from typing import Any
from core.utilities.validators import validate_parameter


central_registry = {
    "goals": {},
}


def _validate_key(key: str | list[str]) -> None:
    if not key:
        raise ValueError(
            "key cannot be empty\n"
            "edge case, the key is most likely an empty list/anything falsy\n"
            f"received: {key}\n"
            f"type: {type(key).__name__}"
        )
    if not isinstance(key, (str, list)):
        raise TypeError(
            "key must be a string or list containing strings\n"
            f"received: {key}\n"
            f"type: {type(key).__name__}"
        )
    if isinstance(key, list) and not all(isinstance(list_item, str) for list_item in key):
        items = []
        for list_item in key:
            validity = isinstance(list_item, str)
            items.append({list_item: validity})
        raise TypeError(
            "all items in key list must be strings\n"
            "items received and their validity :\n"
            f"{items}"
        )


def set_central_registry(
        key: str | list[str],
        obj: Any,
    ) -> None:
    
    _validate_key(key)
    validate_parameter(obj, "obj")

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

def get_central_registry(
        key: str | list[str]
    ):

    _validate_key(key)

    if isinstance(key, str):
        return central_registry[key]
    else:
        ref = central_registry
        for i in key:
            ref = ref[i]
        return ref


if __name__ == "__main__":
    pass