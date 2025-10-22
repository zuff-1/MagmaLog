
import datetime
import engine.clock as clock

def test_new_day_event():
    fake_now = datetime.datetime(
        year=727,
        month=10,
        day=19,
        hour=23,
        minute=59,
        second=50,
    )
    clock.new_day_event_calls.clear()
    clock._current_day = fake_now.date()

    def fake_now_tick():
        nonlocal fake_now
        fake_now += datetime.timedelta(seconds=1)
        return fake_now
    
    feedback = []

    def new_day_event_user():
        feedback.append("used")

    clock.on_new_day(new_day_event_user)
    
    for i in range(15):
        clock.check_new_day(lambda: fake_now)
        fake_now_tick()

    assert feedback == ["used"]