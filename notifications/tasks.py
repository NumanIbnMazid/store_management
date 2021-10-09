from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
from notifications.models import Notification
from studios.models import Studio
from datetime import datetime, date
from django.http import HttpResponse

@shared_task
def notification():
    # Notification updated
    qs = Notification.objects.filter(published_date__lte=datetime.now())
    qs.update(is_published=True)
    return {"status": True}
 
