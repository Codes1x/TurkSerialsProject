import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .models import Series

# Названия сериалов для исключения (захардкожено вручную)
EXCLUDE_TITLES = [
    "Сериал для исключения 1",
    "Сериал для исключения 2",
]

def fetch_turkplaytv_serials():
    base_url = "https://turkplaytv.fun"
    catalog_url = f"{base_url}/all-serial"
    response = requests.get(catalog_url, timeout=10)
    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.text, "html.parser")
    series_links = [a for a in soup.find_all('a', href=True) if "/series-" in a['href']]

    for a in series_links:
        series_url = urljoin(base_url, a['href'])
        if Series.objects.filter(url=series_url).exists():
            continue

        series_page = requests.get(series_url, timeout=10)
        if series_page.status_code != 200:
            continue

        series_soup = BeautifulSoup(series_page.text, "html.parser")

        title_tag = series_soup.find('div', class_='short-cinema__name')
        if not title_tag:
            continue
        title = title_tag.text.strip()

        if title in EXCLUDE_TITLES:
            continue

        desc_block = series_soup.find('div', class_='box-all-text closed')
        description = desc_block.get_text(separator="\n", strip=True) if desc_block else ""

        images = []
        swiper_wrapper = series_soup.find('div', class_='swiper-wrapper')
        if swiper_wrapper:
            imgs = swiper_wrapper.find_all('img', attrs={'data-src': True})
            images = [urljoin(base_url, img['data-src']) for img in imgs]

        Series.objects.create(
            title=title,
            source="TP2",
            url=series_url,
            images=images,
            description=description
        )
        time.sleep(1)


def fetch_tureckiitv_serials():
    base_url = "https://tureckii.tv"
    catalog_url = f"{base_url}/catalog"
    response = requests.get(catalog_url, timeout=10)
    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.text, "html.parser")
    series_links = [a for a in soup.find_all('a', href=True) if "/serial-" in a['href']]

    for a in series_links:
        series_url = urljoin(base_url, a['href'])
        if Series.objects.filter(url=series_url).exists():
            continue

        series_page = requests.get(series_url, timeout=10)
        if series_page.status_code != 200:
            continue

        series_soup = BeautifulSoup(series_page.text, "html.parser")

        title_tag = series_soup.find('div', class_='short-cinema__name')
        if not title_tag:
            continue
        title = title_tag.text.strip()

        if title in EXCLUDE_TITLES:
            continue

        desc_block = series_soup.find('div', class_='box-all-text closed')
        description = desc_block.get_text(separator="\n", strip=True) if desc_block else ""

        images = []
        swiper_wrapper = series_soup.find('div', class_='swiper-wrapper')
        if swiper_wrapper:
            imgs = swiper_wrapper.find_all('img', attrs={'data-src': True})
            images = [urljoin(base_url, img['data-src']) for img in imgs]

        Series.objects.create(
            title=title,
            source="TP4",
            url=series_url,
            images=images,
            description=description
        )
        time.sleep(1)
