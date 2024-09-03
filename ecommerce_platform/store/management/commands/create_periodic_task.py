from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

class Command(BaseCommand):
    help = 'Create a periodic task to import products daily at 2:30 PM'

    def handle(self, *args, **kwargs):
        # Configure the task to run daily at 2:30 PM
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute='30',
            hour='14',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )

        # Ensure periodic task does not already exist
        task_name = 'Import Products Daily at 2:30 PM'
        if not PeriodicTask.objects.filter(name=task_name).exists():
            PeriodicTask.objects.create(
                crontab=schedule,
                name=task_name,
                task='store.tasks.import_products_task',
            )
            self.stdout.write(self.style.SUCCESS('Periodic task created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Periodic task already exists'))
