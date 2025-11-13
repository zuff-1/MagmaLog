from typing import Any, Tuple, Type


def validate_parameter(
        value: Any,
        name: str,
        expected_type: Type | Tuple[Type, ...],
):
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