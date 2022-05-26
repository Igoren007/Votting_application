from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings
from celery import Celery
from . import celeryconfig

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Poll.settings')

app = Celery('Poll',
             broker=celeryconfig.broker_url,
             backend=celeryconfig.result_backend)

app.config_from_object("poll_app.celeryconfig")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))