import os
from datetime import datetime

from celery import Celery
from django.conf import settings

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE','technoparkTimetable.settings'
)

import django
django.setup()


app = Celery('technoparkTimetable')
app.config_from_object(settings.CELERY)

app.conf.broker_connection_retry_on_startup = True
# app.conf.beat_schedule = {}
app.conf.beat_schedule = {
    'update-schedule-1hours' : {
        'task': 'timetable.views.import_shgpu_bot.tasks.import_schedule_from_shspu_bot',
        'schedule': 3600.0,
    },
}
app.autodiscover_tasks()