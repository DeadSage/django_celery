import os
import requests
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task
def handle_uploaded_file(f):
    with open(f'media/documents/{f}') as file:
        res_list = []
        for item in file:

            try:
                res = requests.get(f'http://{item}', timeout=0.1)
                res_list.append(res)

            except (requests.ConnectionError, requests.ConnectTimeout, requests.ReadTimeout):
                continue

        return all([r.status_code == requests.codes.ok for r in res_list])



