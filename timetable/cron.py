from django_cron import CronJobBase, Schedule
from .backup import Command


class BackupJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'timetable.backup_job'

    def do(self):
        Command().handle()
