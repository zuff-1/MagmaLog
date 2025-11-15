

class GoalError(Exception):
    """
    Base class for all goal-related errors.
    """
class GoalAlreadyExistsError(GoalError):
    """
    Raised when trying to create a goal that already exists.
    """


class ValidatorError(Exception):
    """
    Base class for all Validator related errors.
    Raised when the validator was used incorrectly.
    """
class ValidatorHelperError(ValidatorError):
    """
    Raised when a validator helper function was used incorrectly.
    """