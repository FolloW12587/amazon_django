import datetime


class WeekdayFinderMixin:
    def __init__(self, *args, **kwargs):
        pass

    def get_monday(self):
        return self._get_weekday(1)

    def get_tuesday(self):
        return self._get_weekday(2)

    def get_wednesnday(self):
        return self._get_weekday(3)

    def get_thursday(self):
        return self._get_weekday(4)

    def get_friday(self):
        return self._get_weekday(5)

    def get_saturday(self):
        return self._get_weekday(6)

    def get_sunday(self):
        return self._get_weekday(0)

    def check_weekday(self, i, date):
        return date.weekday() == (i - 1)%7 
    
    def _get_weekday(self, i):
        today = datetime.date.today()
        idx = (today.weekday() + 1) % 7 
        return today - datetime.timedelta((idx-i)%7)

    