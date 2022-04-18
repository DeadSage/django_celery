import os
import requests
from celery import Celery
import time
import django
import json
from django.core.files.base import ContentFile

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
    res_dict = {'OK': [], 'NOT_OK': []}
    with open(f'media/{str(f.document)}') as file:
        for item in file:

            try:
                if requests.get(f'http://{item}', timeout=0.1).status_code == requests.codes.ok:
                    res_dict['OK'].append(item)
                else:
                    res_dict['NOT_OK'].append(item)
            except (requests.ConnectionError, requests.ConnectTimeout, requests.ReadTimeout):
                res_dict['NOT_OK'].append(item)
                continue
    f.result.save(name=f'{str(f.document)[:-4]}.json', content=ContentFile(json.dumps(res_dict, indent=4)))
    calc_time = time.time() - start_time
    f.calc_time = calc_time
    f.save()
