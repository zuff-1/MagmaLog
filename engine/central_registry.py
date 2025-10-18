


central_registry = {}


class CentralRegistryControls:

    def set_central_registry(
            key,
            object
            ):
        central_registry[key] = object

    def get_central_registry(key):
        return central_registry.get(key)


if __name__ == "__main__":
    pass