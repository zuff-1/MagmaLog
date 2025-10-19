


central_registry = {}


class CentralRegistryControls():

    def set_central_registry(
            key,
            obj,
    ):
        if isinstance(key, str):
            central_registry[key] = obj
            return
        
        reference = central_registry
        for i in key[:-1]:
            reference = reference[i]
        reference[key[-1]] = obj




    def get_central_registry(key):
        return central_registry.get(key)


if __name__ == "__main__":
    pass