
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
    feedback = []

    def fake_now_tick(**kwarg):
        nonlocal fake_now
        fake_now += datetime.timedelta(**kwarg)

    def dummy_function():
        feedback.append("used")

    def main_sequence():

        clock.on_new_day(dummy_function)

        for i in range(15):
            clock.check_new_day(lambda: fake_now)
            fake_now_tick(seconds=1)
    
    main_sequence()
    assert feedback == ["used"]