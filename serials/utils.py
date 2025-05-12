import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .models import Series

# Список названий сериалов, которые не нужно сохранять (исключения)
EXCLUDE_TITLES = [
    # Добавьте названия сериалов для исключения здесь, например:
    # "Название сериала 1", "Название сериала 2"
]

def fetch_turkplaytv_serials():
    """Парсит список сериалов с TurkPlayTV (TP2) и сохраняет новые сериалы в базу."""
    base_url = "https://turkplaytv.fun"
    catalog_url = f"{base_url}/all-serial"
    try:
        response = requests.get(catalog_url, timeout=10)
    except Exception as e:
        print(f"Ошибка подключения к {catalog_url}: {e}")
        return
    if response.status_code != 200:
        print(f"Не удалось получить данные с {catalog_url}, статус: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    # Находим все ссылки на страницы сериалов (ссылка содержит "/series-")
    series_links = [a for a in soup.find_all('a', href=True) if "/series-" in a['href']]
    for a in series_links:
        title = a.get_text(strip=True)
        # Удаляем префикс "новинка!" из названия, если присутствует
        if title.lower().startswith("новинка"):
            title = title.split("новинка!", 1)[-1].strip()
        series_url = urljoin(base_url, a['href'])
        # Пропускаем, если сериал уже есть в базе или название в списке исключений
        if title in EXCLUDE_TITLES or Series.objects.filter(url=series_url).exists():
            continue

        # Загружаем страницу конкретного сериала для получения деталей
        try:
            page = requests.get(series_url, timeout=10)
        except Exception as e:
            print(f"Не удалось получить страницу {series_url}: {e}")
            continue
        if page.status_code != 200:
            print(f"Ошибка загрузки {series_url}, статус: {page.status_code}")
            continue

        soup_series = BeautifulSoup(page.text, "html.parser")
        # Название сериала
        name_tag = soup_series.find('div', class_='short-cinema__name')
        title_detail = name_tag.get_text(strip=True) if name_tag else title
        # Описание сериала
        desc_tag = soup_series.find('div', class_='box-all-text')
        if not desc_tag:
            desc_tag = soup_series.find('div', class_='box-all-text closed')
        description = desc_tag.get_text(strip=True, separator="\n") if desc_tag else ""
        # Список изображений сериала
        images = []
        img_container = soup_series.find('div', class_='swiper-wrapper')
        if img_container:
            for img in img_container.find_all('img'):
                # Берем URL из data-src (если нет, то из src)
                img_url = img.get('data-src') or img.get('src')
                if img_url:
                    img_url = urljoin(base_url, img_url)
                    images.append(img_url)
        # Сохраняем сериал в базу данных
        Series.objects.create(
            title=title_detail,
            source="TP2",
            url=series_url,
            images=images,
            description=description
        )
        # Плавная задержка между запросами
        time.sleep(1)


def fetch_tureckiitv_serials():
    """Парсит список сериалов с TureckiiTV (TP4) и сохраняет новые сериалы в базу."""
    base_url = "https://tureckii.tv"
    catalog_url = f"{base_url}/catalog"
    try:
        response = requests.get(catalog_url, timeout=10)
    except Exception as e:
        print(f"Ошибка подключения к {catalog_url}: {e}")
        return
    if response.status_code != 200:
        print(f"Не удалось получить данные с {catalog_url}, статус: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    # Находим все ссылки на страницы сериалов (ссылка содержит "/serial-")
    series_links = [a for a in soup.find_all('a', href=True) if "/serial-" in a['href']]
    for a in series_links:
        title = a.get_text(strip=True)
        # Удаляем префикс "новинка!" из названия, если есть
        if title.lower().startswith("новинка"):
            title = title.split("новинка!", 1)[-1].strip()
        series_url = urljoin(base_url, a['href'])
        # Пропускаем сериал, если он уже есть или в списке исключенных
        if title in EXCLUDE_TITLES or Series.objects.filter(url=series_url).exists():
            continue

        # Загружаем страницу сериала для получения деталей
        try:
            page = requests.get(series_url, timeout=10)
        except Exception as e:
            print(f"Не удалось получить страницу {series_url}: {e}")
            continue
        if page.status_code != 200:
            print(f"Ошибка загрузки {series_url}, статус: {page.status_code}")
            continue

        soup_series = BeautifulSoup(page.text, "html.parser")
        # Название сериала
        name_tag = soup_series.find('div', class_='short-cinema__name')
        title_detail = name_tag.get_text(strip=True) if name_tag else title
        # Описание сериала
        desc_tag = soup_series.find('div', class_='box-all-text')
        if not desc_tag:
            desc_tag = soup_series.find('div', class_='box-all-text closed')
        description = desc_tag.get_text(strip=True, separator="\n") if desc_tag else ""
        # Список URL изображений
        images = []
        img_container = soup_series.find('div', class_='swiper-wrapper')
        if img_container:
            for img in img_container.find_all('img'):
                img_url = img.get('data-src') or img.get('src')
                if img_url:
                    img_url = urljoin(base_url, img_url)
                    images.append(img_url)
        # Сохраняем информацию о сериале в базе
        Series.objects.create(
            title=title_detail,
            source="TP4",
            url=series_url,
            images=images,
            description=description
        )
        # Задержка между запросами
        time.sleep(1)
