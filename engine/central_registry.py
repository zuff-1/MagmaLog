

central_registry = {}


class CentralRegistryControls():

    def set_central_registry(
            key,
            obj,
    ):
        def set_non_nested_key():
            central_registry[key] = obj
            return
        
        def set_nested_key():
            ref = central_registry
            for i in key[:-1]:
                ref = ref[i]
            ref[key[-1]] = obj
        
        def main_sequence():
            if isinstance(key, str):
                set_non_nested_key()
            else:
                set_nested_key()
        
        main_sequence()


    def get_central_registry(key):
        ref = central_registry

        if isinstance(key, str):
            return ref[key]
        
        for i in key:
            ref = ref[i]
        return ref              #chop chop in weekend

if __name__ == "__main__":
    pass