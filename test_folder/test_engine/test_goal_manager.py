from core.engine import goal_manager as goal_manager
import datetime

user_goal = (
goal_manager.
UserGoal(
    name = "code",
    target_duration = 7200,
)
)

def test_add_goal_progress():
    today = datetime.date.today()
    key = today.isoformat()
    user_goal.add_goal_progress(hours=4)
    assert user_goal.dict[key]["is_achieved"]
    assert user_goal.dict[key]["action_duration"] == (4*60*60)

    fake_date = datetime.date(727, 2, 7)
    fake_key = fake_date.isoformat()
    user_goal.add_goal_progress(date_provider=lambda:fake_date, hours=1)
    assert not user_goal.dict[fake_key]["is_achieved"]
    assert user_goal.dict[fake_key]["action_duration"] == (1*60*60)
