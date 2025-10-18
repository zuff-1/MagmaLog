import engine.goal_manager


name = "Code"
goal_duration = 7200

user_goal = (
engine.
goal_manager.
UserGoal(
    name,
    goal_duration,
    )
)

def test_constructor():
    assert user_goal.name == name
    assert user_goal.goal_duration == goal_duration
    assert user_goal.goal_duration_progress == 0
    assert user_goal.dict == {}

def test_log_duration_progress():
    duration_progress = 120
    user_goal.log_duration_progress(duration_progress)
    assert user_goal.goal_duration_progress == duration_progress





