from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from . import celeryconfig

app = Celery('mive')
app.config_from_object(celeryconfig)
app.autodiscover_tasks()
