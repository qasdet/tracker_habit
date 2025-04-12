import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')

app = Celery('habit_tracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-habits-daily': {
        'task': 'telegram_bot.tasks.check_habits_and_send_reminders',
        'schedule': crontab(minute='*/1'),  # Каждую минуту
    },
}