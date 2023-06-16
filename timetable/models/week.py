from datetime import date, timedelta
from django.db import models


class Week(models.Model):
    start_day = models.DateField()
    end_day = models.DateField()

    @classmethod
    def create_weeks_for_current_year(cls):
        current_year = date.today().year
        existing_weeks = cls.objects.filter(start_day__year=current_year)

        if existing_weeks.exists():
            print("Weeks for the current year already exist. Skipping creation.")
            return

        weeks = []
        start_date = date(current_year, 1, 1)
        while start_date.weekday() != 0:  # Находим первый понедельник
            start_date += timedelta(days=1)

        while start_date.year == current_year:
            end_date = start_date + timedelta(days=6)
            week = cls(start_day=start_date, end_day=end_date)
            weeks.append(week)
            start_date += timedelta(days=7)

        cls.objects.bulk_create(weeks)

    def __str__(self):
        return f"Week {self.start_day} - {self.end_day}"
