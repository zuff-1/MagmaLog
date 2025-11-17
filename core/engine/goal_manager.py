from typing import Callable
import datetime


from core.engine import central_registry as central_registry
from core.utilities.validators import validate_parameter, validate_callable
from core.exceptions import GoalAlreadyExistsError


class UserGoal():

    def __init__(
            self,
            name: str,
            target_duration: int,
            description: str,
    ) -> None:
        
        validate_parameter(name, "name", str)
        validate_parameter(target_duration, "target_duration", int)
        validate_parameter(description, "description", str)
        if name in central_registry.central_registry["goals"]:
            raise GoalAlreadyExistsError(
                "a goal with the same name already exists in the central_registry\n"
                f"received name: {name}"
            )

        self.name = name
        self.target_duration = target_duration
        self.description = description

        self.data = {}
        self.date_created = datetime.date.today().isoformat()
        central_registry.set_central_registry(["goals", name], self)

    def add_goal_progress(
            self,
            progress_seconds: int,
            date_provider: Callable[[],datetime.date] | None = None,
            ) -> None:
        
        validate_parameter(progress_seconds, "progress_seconds", int)

        if date_provider is not None:
            validate_callable(date_provider, "date_provider")
            
            result = date_provider()
            if not isinstance(result, datetime.date):
                raise TypeError(
                    "date_provider must return a datetime.date object"
                    f"received: {result}"
                    f"type: {type(result)}"
                )
        else:
            date_provider = datetime.date.today

        today = date_provider()
        key = today.isoformat()
        progress = progress_seconds

        if key in self.data:
            saved_progress = self.data[key]["action_duration"]
            progress += saved_progress
            self.data[key]["action_duration"] = progress

            if (
                not self.data[key]["is_achieved"]
                and self.data[key]["action_duration"] >= self.data[key]["target_duration"]
            ):
                self.data[key]["is_achieved"] = True
                
        else:
            is_achieved = progress >= self.target_duration
            self.data[key] = {
                "date": key,
                "action_duration": progress,
                "target_duration": self.target_duration,
                "is_achieved": is_achieved,
            }
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "target_duration": self.target_duration,
            "description": self.description,

            "data": self.data,
            "date_created": self.date_created,
        }
    
    @classmethod
    def from_dict(cls, data):
        goal = cls.__new__(cls)

        goal.name = data["name"]
        goal.target_duration = data["target_duration"]
        goal.description = data["description"]      

        goal.data = data["data"]
        goal.date_created = data["date_created"]
        central_registry.set_central_registry(["goals", data["name"]], goal)