import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .models import Series
from django.utils.timezone import now
from django.core.cache import cache

# Ключ кеша для логирования последнего парсинга
LAST_PARSE_CACHE_KEY = "last_parse_timestamp"

# Получение списка исключений из Google Docs (текстовая версия)
def get_excluded_titles():
    url = "https://docs.google.com/document/d/1C4dAriMzsTH8ppppXq3N00Lcy5G_9_HsjEr4kkRyuSw/export?format=txt"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return set(title.strip() for title in response.text.splitlines() if title.strip())
    except Exception as e:
        print("Ошибка при получении исключений:", e)
    return set()


def fetch_turkplaytv_serials(excluded_titles):
    base_url = "https://turkplaytv.fun"
    catalog_url = f"{base_url}/all-serial"
    try:
        response = requests.get(catalog_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("Ошибка загрузки каталога TP2:", e)
        return

    soup = BeautifulSoup(response.text, "html.parser")
    series_links = [a for a in soup.find_all('a', href=True) if "/series-" in a['href']]

    for a in series_links:
        series_url = urljoin(base_url, a['href'])
        if Series.objects.filter(url=series_url).exists():
            continue

        try:
            page = requests.get(series_url, timeout=10)
            page.raise_for_status()
        except Exception:
            continue

        soup_series = BeautifulSoup(page.text, "html.parser")
        title_tag = soup_series.find('div', class_='short-cinema__name')
        title = title_tag.text.strip() if title_tag else None
        if not title or title in excluded_titles:
            continue

        desc_block = soup_series.find('div', class_='box-all-text closed')
        description = desc_block.get_text(separator="\n", strip=True) if desc_block else ""

        images = []
        swiper = soup_series.find('div', class_='swiper-wrapper')
        if swiper:
            images = [
                urljoin(base_url, img['data-src'])
                for img in swiper.find_all('img', attrs={'data-src': True})
            ]

        Series.objects.create(
            title=title,
            source="TP2",
            url=series_url,
            images=images,
            description=description,
            is_active=True
        )
        time.sleep(1)


def fetch_tureckiitv_serials(excluded_titles):
    base_url = "https://tureckii.tv"
    catalog_url = f"{base_url}/catalog"
    try:
        response = requests.get(catalog_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("Ошибка загрузки каталога TP3:", e)
        return

    soup = BeautifulSoup(response.text, "html.parser")
    series_links = [a for a in soup.find_all('a', href=True) if "/serial-" in a['href']]

    for a in series_links:
        series_url = urljoin(base_url, a['href'])
        if Series.objects.filter(url=series_url).exists():
            continue

        try:
            page = requests.get(series_url, timeout=10)
            page.raise_for_status()
        except Exception:
            continue

        soup_series = BeautifulSoup(page.text, "html.parser")
        title_tag = soup_series.find('div', class_='short-cinema__name')
        title = title_tag.text.strip() if title_tag else None
        if not title or title in excluded_titles:
            continue

        desc_block = soup_series.find('div', class_='box-all-text closed')
        description = desc_block.get_text(separator="\n", strip=True) if desc_block else ""

        images = []
        swiper = soup_series.find('div', class_='swiper-wrapper')
        if swiper:
            images = [
                urljoin(base_url, img['data-src'])
                for img in swiper.find_all('img', attrs={'data-src': True})
            ]

        Series.objects.create(
            title=title,
            source="TP3",
            url=series_url,
            images=images,
            description=description,
            is_active=True
        )
        time.sleep(1)


def run_full_parsing():
    excluded = get_excluded_titles()
    fetch_turkplaytv_serials(excluded)
    fetch_tureckiitv_serials(excluded)
    # Записываем время последнего парсинга
    cache.set(LAST_PARSE_CACHE_KEY, now().isoformat())
