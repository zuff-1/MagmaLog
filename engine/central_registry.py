


central_registry = {}


class CentralRegistryControls():

    def set_central_registry(
            key,
            obj,
    ):
        if isinstance(key, str):
            central_registry[key] = obj
            return
        
        ref = central_registry
        for i in key[:-1]:
            ref = ref[i]
        ref[key[-1]] = obj


    def get_central_registry(key):
        ref = central_registry

        if isinstance(key, str):
            return ref[key]
        
        for i in key:
            ref = ref[i]
        return ref

if __name__ == "__main__":
    pass