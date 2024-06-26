from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()




















"""
import os
from celery import Celery
from django.conf import settings
from celery import shared_task

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('backend', broker=settings.BROKER_URL)

# Configure Celery
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.broker_url ="amqp://nisira:bidjango.@localhost"

@shared_task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@shared_task
def sample_task():
    print("The sample task just ran.")
"""


