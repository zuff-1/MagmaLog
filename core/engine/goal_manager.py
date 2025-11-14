from typing import Callable
import datetime


from core.validators import validate_parameter
from core.engine import central_registry as central_registry

#unfinished

class UserGoal():

    def __init__(
            self,
            name: str,
            target_duration: int,
            description: str,
    ):
        validate_parameter(value=name, expected_type=str, name="name")
        if not isinstance(target_duration, int):
            raise TypeError(
                "target_duration must be an integer\n"
                f"received: {target_duration}\n"
                f"type: {type(target_duration).__name__}"
            )
        if not target_duration:
            raise ValueError(
                "target_duration cannot be falsy\n"
                f"received: {name}\n"
                f"type: {type(name).__name__}"
            )
        if not isinstance(description, str):
            raise TypeError(
                "description must be a string\n"
                f"received: {name}\n"
                f"type: {type(name).__name__}"
            )

        self.name = name
        self.target_duration = target_duration
        self.description = description

        self.data = {}
        self.date_created = datetime.date.today().isoformat()
        central_registry.set_central_registry(["goals", name], self)

    def add_goal_progress(
            self,
            date_provider: Callable[[],datetime.date],
            progress_seconds: int = 0,
            ) -> None:
        if not callable(date_provider):
            raise TypeError(
                "date_provider must be a callable\n"
                f"received: {date_provider}"
                f"type: {type(date_provider).__name__}"
            )
        result = date_provider()
        if not isinstance(result, datetime.date):
            raise TypeError(
                "date_provider must return a datetime.date object"
                f"received: {result}"
                f"type: {type(result)}"
            )
        if not isinstance(progress_seconds, int):
            raise TypeError(
                "progress_seconds must be an integer\n"
                f"received: {progress_seconds}\n"
                f"type: {type(progress_seconds).__name__}"
            )

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