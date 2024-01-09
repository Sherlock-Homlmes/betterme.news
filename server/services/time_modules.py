# default
import datetime

# libraries
import pytz


def vn_now() -> datetime.datetime:
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Asia/Ho_Chi_Minh"))
    now = datetime.datetime(pst_now.year, pst_now.month, pst_now.day, pst_now.hour, pst_now.minute)
    return now


def time_to_str(t: datetime.datetime) -> str:
    return t.strftime("%Y-%m-%d %H:%M:%S")


def str_to_time(s: str) -> datetime.datetime:
    return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


class Time:
    def __init__(self):
        now: datetime.datetime = vn_now()
        self.now: datetime.datetime = now
        self.today: datetime.datetime = datetime.datetime(now.year, now.month, now.day)

    def some_day_before(self, days: int) -> datetime.datetime:
        that_day = self.now - datetime.timedelta(days=days)
        return datetime.datetime(that_day.year, that_day.month, that_day.day)

    def some_day_after(self, days: int) -> datetime.datetime:
        that_day = self.now + datetime.timedelta(days=days)
        return datetime.datetime(that_day.year, that_day.month, that_day.day)


# test time module
# time1=str_to_time('2023-03-20 23:38:00')
# midnight=Now().some_day_before(0)
# time2=str_to_time('2023-03-22 21:17:00')
# def timedelta_to_daily_list(time1: datetime.datetime, time2: datetime.datetime):
#     time2_hour = time2.hour
#     if time2.hour != time1.hour or time1.day != time2.day:
#         if time2.hour == 0:
#             time2_hour = 24
#         study_time = [
#             (lambda x: 60 if (x > time1.hour and x < time2_hour) else 0)(x)
#             for x in range(0, 24)
#         ]
#         if time2_hour != 24:
#             study_time[time2.hour] = time2.minute
#         if not study_time[time1.hour]:
#             study_time[time1.hour] = 60 - time1.minute
#     elif time1.hour == time2.hour:
#         study_time = [0] * 24
#         study_time[time2_hour] = time2.minute - time1.minute
#     return study_time

# print(timedelta_to_daily_list(time1, midnight))
# print(timedelta_to_daily_list(midnight, time2))
