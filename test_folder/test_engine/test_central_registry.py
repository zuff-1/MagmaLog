from engine import central_registry as central_registry


def test_set_central_registry():
    (
    central_registry.
    CentralRegistryControls.
    set_central_registry(
        key="key1",
        obj={"key2": "test item"},
    )
    )
    assert central_registry.central_registry["key1"] == {"key2": "test item"}

def test_get_central_registry():
    item = (
    central_registry.
    CentralRegistryControls.
    get_central_registry(
        key=["key1", "key2"]
    )
    )
    assert item == "test item"

