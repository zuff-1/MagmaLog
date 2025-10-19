
from datetime import datetime


class UserGoal():

    def __init__(
            self,
            name,
            goal_duration,
    ):
        self.name = name
        self.goal_duration = goal_duration
        self.goal_duration_progress = 0
        self.goal_counter = 0
        self.dict = {}

    def log_duration_progress(
            self,
            duration_progress = 0,
    ):
        self.goal_duration_progress += duration_progress

    def log_day(
            self,
            ):
        present = datetime.now()
        present_date = present.date

        #unfinished
        pass