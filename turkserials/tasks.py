from celery import shared_task
from . import utils

@shared_task
def parse_all_series():
    """Фоновая задача Celery для парсинга сериалов с TurkPlayTV (TP2) и TureckiiTV (TP4)."""
    # Вызываем парсеры для обоих сайтов
    utils.fetch_turkplaytv_serials()
    utils.fetch_tureckiitv_serials()
