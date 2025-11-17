import pkgutil
import importlib

# Automatically import all submodules in this package
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__, prefix=__name__ + "."):
    importlib.import_module(module_name)