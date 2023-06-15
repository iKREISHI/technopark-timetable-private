from django.core.management.base import BaseCommand
from django.core import management


class Command(BaseCommand):
    help = 'Creates a backup of the database.'

    def handle(self, *args, **options):
        management.call_command('dbbackup')
