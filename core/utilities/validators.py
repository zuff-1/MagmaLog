

from typing import Any, Tuple, Type, Iterable, Callable


from core.exceptions import ValidatorHelperError, ValidatorError


def _validate_type_or_tuple(
        value: Type | Tuple[Type, ...],
        label: str,
    ) -> None:

    if not isinstance(label, str):
        raise ValidatorHelperError(
            "label must be a string"
            f"received: {label}"
            f"type: {type(label).__name__}"
        )
    
    if isinstance(value, Type):
        return True
    if isinstance(value, Tuple) and all(isinstance(element, Type) for element in value):
        return True
    
    raise ValidatorError(
        f"{label} must be type or a tuple of types (also cannot be None)\n"
        f"received: {value}\n"
        f"type: {type(value).__name__}"
    )

def validate_parameter(
        value: Any,
        label: str,
        expected_type: Type | Tuple[Type, ...] | None = None,
        element_type: Type | Tuple[Type, ...] | None = None,
    ) -> None:

    if not isinstance(label, str):
        raise ValidatorError(
            "label of the parameter has to be string\n"
            f"received: {label}\n"
            f"type: {type(label).__name__}"
        )
    
    if expected_type is not None:
        _validate_type_or_tuple(expected_type, "expected_type")

        if not isinstance(value, expected_type):
            raise TypeError(
                f"{label} type must be {expected_type}\n"
                f"received: {value}\n"
                f"type: {type(value).__name__}"
            )
        
    if not value:
        raise ValueError(
            f"{label} cannot be falsy\n"
            f"received: {value}\n"
            f"type: {type(value).__name__}"
        )
    if (
        element_type is not None
        and not isinstance(value, (str, bytes))
        and isinstance(value, Iterable)
        ):
        _validate_type_or_tuple(element_type, "element_type")

        for element in value:
            if not isinstance(element, element_type):
                raise TypeError(
                    f"{label} iterable failed elements check, has an invalid element\n"
                    f"{label} iterable value: {value}\n"
                    f"invalid element: {element}\n"
                    f"invalid element type: {type(element).__name__}"
                )

def validate_callable(
        func: Callable,
        label: str,
    ) -> None:
    
    try:
        validate_parameter(label, "label", str)
    except TypeError:
        raise ValidatorError(
            "label must be a string type"
            f"received: {label}"
            f"type: {type(label).__name__}"
        )

    if not callable(func):
        raise TypeError(
            f"{label} must be a callable\n"
            f"received: {repr(func)}\n"
            f"type: {type(func).__name__}"
        )