

central_registry = {
    "goals": {},
}


def set_central_registry(key: list, obj):
    if not key:
        raise ValueError(
            "Key cannot be empty"
            "edge case, the key is most likely an empty list/anything falsy."
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

def get_central_registry(key):
    ref = central_registry

    if isinstance(key, str):
        return ref[key]
    else:
        for i in key:
            ref = ref[i]
        return ref

if __name__ == "__main__":
    pass