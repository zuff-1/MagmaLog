

from typing import Any, Tuple, Type, Iterable


def _validate_type_or_tuple(
        x: Type | Tuple[Type, ...],
        label: str,
        ):
    if not isinstance(label, str):
        raise TypeError(
            "validator helper error, label must be a string"
            f"received: {label}"
            f"type: {type(label).__name__}"
        )
    if isinstance(x, Type):
        return True
    if isinstance(x, Tuple) and all(isinstance(element, Type) for element in x):
        return True
    raise TypeError(
        f"validator error, {label} must be type or a tuple of types (also cannot be None)\n"
        f"received: {x}\n"
        f"type: {type(x).__name__}"
    )

def validate_parameter(
        value: Any,
        name: str,
        expected_type: Type | Tuple[Type, ...],
        element_type: Type | Tuple[Type, ...] | None = None,
):  
    _validate_type_or_tuple(expected_type, "expected_type")
    if not isinstance(name, str):
        raise TypeError(
            "validator error, name of parameter has to be string\n"
            f"received: {name}\n"
            f"type: {type(name).__name__}"
        )
    if not isinstance(value, expected_type):
        raise TypeError(
            f"{name} type must be {expected_type}\n"
            f"received: {value}\n"
            f"type: {type(value).__name__}"
        )
    if element_type is not None:
        _validate_type_or_tuple(element_type, "element_type")
        if not isinstance(value, Iterable) or isinstance(value, (str, bytes)):
            raise TypeError(
                f"validator error for {name}, value must be a non string iterable "
                f"received: {value}"
                f"type: {type(value).__name__}"
            )
        for element in value:
            if not isinstance(element, element_type):
                raise TypeError(
                    "iterable value has an invalid element"
                    f"iterable value: {value}"
                    f"invalid element: {element}"
                )
    if not value:
        raise ValueError(
            f"{name} cannot be falsy\n"
            f"received: {value}\n"
            f"type: {type(value).__name__}"
        )
    
