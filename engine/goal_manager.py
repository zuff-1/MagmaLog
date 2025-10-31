
import datetime


class UserGoal():

    def __init__(
            self,
            name,
            target_duration,
    ):
        self.name = name
        self.target_duration = target_duration
        self.target_duration_progress = 0
        self.dict = {}


    def day_end():

        # remember, if u use datetime.now here,
        # it pastes the next day instead,
        # not the ended day.
        # As serie said use -timedelta(days=1).

        pass