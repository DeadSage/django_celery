import os
import requests
from celery import Celery
import time
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

from url_check.models import Document


@app.task
def handle_uploaded_file():
    start_time = time.time()
    f = Document.objects.last()
    with open(f'media/{str(f.document)}') as file:
        res_list = []
        for item in file:

            try:
                res = requests.get(f'http://{item}', timeout=0.1)
                res_list.append(res)

            except (requests.ConnectionError, requests.ConnectTimeout, requests.ReadTimeout):
                continue
    res = all([r.status_code == requests.codes.ok for r in res_list])
    calc_time = time.time() - start_time
    f.result = res
    f.calc_time = calc_time
    f.save()
