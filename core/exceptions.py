

class GoalError(Exception):
    """
    Base class for all goal-related errors.
    """
    pass

class GoalAlreadyExistsError(GoalError):
    """
    Raised when trying to create a goal that already exists.
    """
    pass