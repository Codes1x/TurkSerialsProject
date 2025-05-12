from django.core.management.base import BaseCommand
from serials import utils

class Command(BaseCommand):
    help = "Parse series from TurkPlayTV (TP2) and TureckiiTV (TP4)"

    def handle(self, *args, **options):
        # Запуск парсеров для обоих сайтов
        utils.fetch_turkplaytv_serials()
        utils.fetch_tureckiitv_serials()
        # Сообщение об успешном завершении
        self.stdout.write(self.style.SUCCESS("Парсинг сериалов завершен."))
