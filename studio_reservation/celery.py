import os
from datetime import datetime, timedelta
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studio_reservation.settings.development')

app = Celery('studio_reservation')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

datetime_now = datetime.now()
app.conf.beat_schedule = {
    'add-every-6-hours': {
        'task': 'notifications.tasks.notification',
        'schedule': timedelta(hours=6),
    }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')