import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def download_images(url, output_folder):
    # Получаем HTML-код страницы
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Создаем папку для сохранения изображений, если ее нет
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Находим все теги <img> на странице
    img_tags = soup.find_all('img')

    for img_tag in img_tags:
        # Получаем URL изображения
        img_url = img_tag.get('src')

        # Избегаем пустых URL
        if img_url:
            # Собираем абсолютный URL из относительного, если необходимо
            img_url = urljoin(url, img_url)

            # Получаем имя файла из URL
            img_name = os.path.basename(urlparse(img_url).path)

            # Скачиваем изображение
            img_data = requests.get(img_url).content
            img_path = os.path.join(output_folder, img_name)

            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)

            print(f"Изображение {img_name} успешно скачано.")

# Замените URL страницы и папку вывода по вашему выбору
url_to_scrape = "https://www.praktycznyegzamin.pl/inf03ee09e14/teoria/wszystko/"
output_folder_path = "downloaded_images"

download_images(url_to_scrape, output_folder_path)
