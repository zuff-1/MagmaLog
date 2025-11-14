

from typing import Any, Tuple, Type, Iterable, Callable


def _validate_type_or_tuple(
        value: Type | Tuple[Type, ...],
        label: str,
    ) -> None:

    if not isinstance(label, str):
        raise TypeError(
            "validator helper error, label must be a string"
            f"received: {label}"
            f"type: {type(label).__name__}"
        )
    
    if isinstance(value, Type):
        return True
    if isinstance(value, Tuple) and all(isinstance(element, Type) for element in value):
        return True
    
    raise TypeError(
        f"validator error, {label} must be type or a tuple of types (also cannot be None)\n"
        f"received: {value}\n"
        f"type: {type(value).__name__}"
    )

def validate_parameter(
        value: Any,
        name: str,
        expected_type: Type | Tuple[Type, ...] | None = None,
        element_type: Type | Tuple[Type, ...] | None = None,
    ) -> None:

    if not isinstance(name, str):
        raise TypeError(
            "validator error, name of parameter has to be string\n"
            f"received: {name}\n"
            f"type: {type(name).__name__}"
        )
    
    if expected_type is not None:
        _validate_type_or_tuple(expected_type, "expected_type")

        if not isinstance(value, expected_type):
            raise TypeError(
                f"{name} type must be {expected_type}\n"
                f"received: {value}\n"
                f"type: {type(value).__name__}"
            )
        
    if not value:
        raise ValueError(
            f"{name} cannot be falsy\n"
            f"received: {value}\n"
            f"type: {type(value).__name__}"
        )
    if element_type is not None:
        _validate_type_or_tuple(element_type, "element_type")

        if not isinstance(value, Iterable) or isinstance(value, (str, bytes)):
            raise TypeError(
                f"validator error for {name} elements check\n"
                f"{name} is not iterable, must be a non string iterable\n"
                f"received: {value}\n"
                f"type: {type(value).__name__}"
            )
        for element in value:
            if not isinstance(element, element_type):
                raise TypeError(
                    "iterable value has an invalid element type\n"
                    f"iterable value: {value}\n"
                    f"invalid element: {element}\n"
                    f"invalid element type: {type(element).__name__}"
                )

def validate_callable(
        func: Callable,
        name: str,
    ) -> None:
    
    validate_parameter(name, "name", str)

    if not callable(func):
        raise TypeError(
            f"{name} must be a callable\n"
            f"received: {repr(func)}\n"
            f"type: {type(func).__name__}"
        )