from celery import shared_task
from .utils import fetch_turkplaytv_serials, fetch_tureckiitv_serials

@shared_task
def parse_all_series():
    fetch_turkplaytv_serials()
    fetch_tureckiitv_serials()
