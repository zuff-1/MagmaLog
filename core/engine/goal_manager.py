from typing import Callable
import datetime


from core.engine import central_registry as central_registry


class UserGoal():

    def __init__(
            self,
            name: str,
            target_duration: int,
    ):
        if not isinstance(name, str):
            raise TypeError(
                "name must be a string\n"
                f"received: {name}\n"
                f"type: {type(name).__name__}"
            )
        if not isinstance(target_duration, int):
            raise TypeError(
                "target_duration must be an integer\n"
                f"received: {target_duration}\n"
                f"type: {type(target_duration).__name__}"
            )

        self.name = name
        self.target_duration = target_duration
        self.dict = {}
        central_registry.set_central_registry(["goals", name], self)

    def add_goal_progress(
            self,
            date_provider: Callable[[],datetime.date],
            progress_seconds: int = 0,
            ):
        if not callable(date_provider):
            raise TypeError(
                "date_provider must be a callable\n"
                f"received: {date_provider}"
                f"type: {type(date_provider).__name__}"
            )
        #to be made: check if it returns the correct object

        if not isinstance(progress_seconds, int):
            raise TypeError(
                "progress_seconds must be an integer\n"
                f"received: {progress_seconds}\n"
                f"type: {type(progress_seconds).__name__}"
            )

        today = date_provider()
        key = today.isoformat()
        progress = progress_seconds

        if key in self.dict:
            saved_progress = self.dict[key]["action_duration"]
            progress += saved_progress
            self.dict[key]["action_duration"] = progress
            if (
                not self.dict[key]["is_achieved"]
                and self.dict[key]["action_duration"] >= self.dict[key]["target_duration"]
            ):
                self.dict[key]["is_achieved"] = True
        
        else:
            is_achieved = progress >= self.target_duration
            self.dict[key] = {
                "date": key,
                "action_duration": progress,
                "target_duration": self.target_duration,
                "is_achieved": is_achieved,
            }
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "target_duration": self.target_duration,
            "data": self.dict
        }
    
    @classmethod
    def from_dict(cls, data):
        goal = cls(
            name = data["name"],
            target_duration = data["target_duration"]
        )
        goal.dict = data["data"]
        return goal