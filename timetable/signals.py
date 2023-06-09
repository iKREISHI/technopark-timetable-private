from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from timetable.models.week import Week


@receiver(post_migrate, sender=AppConfig)
def create_weeks(sender, **kwargs):
    Week.create_weeks_for_current_year()
