import requests
from bs4 import BeautifulSoup
import pandas as pd

# Замените на URL веб-сайта, с которого вы хотите извлечь информацию
url = "https://russpass.ru/tours"

# Отправьте запрос GET на веб-сайт и получите HTML-контент
response = requests.get(url)
html_content = response.text

# Создайте объект BeautifulSoup для анализа HTML
soup = BeautifulSoup(html_content, "html.parser")

# Найдите все туристические пакеты на веб-странице
tour_packages = soup.find_all("div", class_="tour-package")

# Извлеките информацию о каждом туристическом пакете
tour_data = []

for package in tour_packages:
    name = package.find("h3", class_="package-name").text
    category = package.find("div", class_="package-category").text
    price = float(package.find("div", class_="package-price").text.strip("$"))
    duration = int(package.find("div", class_="package-duration").text.strip(" days"))

    tour_data.append({"name": name, "category": category, "price": price, "duration": duration})

# Сохраните извлеченную информацию в DataFrame
tour_data_df = pd.DataFrame(tour_data)

# Сохраните данные в CSV-файл
tour_data_df.to_csv("tour_data.csv", index=False)
