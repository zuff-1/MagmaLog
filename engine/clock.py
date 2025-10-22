
import datetime
import time


new_day_event_calls = []
_current_day = datetime.date.today()


def on_new_day(function):
    new_day_event_calls.append(function)

def check_new_day(now_provider = datetime.datetime.now):
    now = now_provider()
    global _current_day

    if now.date() != _current_day:
            _current_day = now.date()

            for function in new_day_event_calls:
                function()

def start_clock():
     while True:
          check_new_day()
          time.sleep(1)





