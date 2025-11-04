from engine import clock
import datetime


class UserGoal():

    def __init__(
            self,
            name,
            target_duration,
    ):
        self.name = name
        self.target_duration = target_duration
        self.dict = {}

    def add_goal_progress(
            self,
            date_provider=datetime.date.today,
            seconds=0,
            minutes=0,
            hours=0,
            ):
        today = date_provider()
        key = today.isoformat()
        progress = (
            (seconds)
            + (minutes * 60)
            + (hours * 3600)
        )
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