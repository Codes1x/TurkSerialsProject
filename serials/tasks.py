from celery import shared_task
from .utils import fetch_turkplaytv_serials, fetch_tureckiitv_serials
from .models import Series
import requests

@shared_task
def periodic_parse_serials():
    exceptions_url = "https://docs.google.com/document/d/1C4dAriMzsTH8ppppXq3N00Lcy5G_9_HsjEr4kkRyuSw/export?format=txt"
    response = requests.get(exceptions_url)
    exceptions_list = response.text.splitlines()

    fetch_turkplaytv_serials(exceptions_list)
    fetch_tureckiitv_serials(exceptions_list)