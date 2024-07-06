import requests
import re
import html
import json
import csv


def get_job_data():
    # URL первой страницы вакансий
    url = "https://www.lejobadequat.com/emplois"

    # Отправка GET-запроса для получения HTML-контента страницы
    response = requests.get(url)
    print('Status code:', response.status_code)

    if response.status_code == 200:
        html_content = response.text

        # Регулярное выражение для извлечения данных вакансий
        job_pattern = re.compile(
            r'<article[^>]*?>.*?<div class="job_secteur_title">(.*?)</div>'
            r'.*?<h3 class="jobCard_title">(.*?)</h3>'
            r'.*?<span><i class="icon-marker"></i>\s*(.*?)\s*</span>',
            re.DOTALL
        )

        # Извлечение данных вакансий
        jobs = job_pattern.findall(html_content)

        job_list = []
        for j in jobs:
            category = re.sub(r'<wbr>', '', j[0].strip())
            title = re.sub(r'<wbr>', '', j[1].strip())
            location = re.sub(r'<wbr>', '', j[2].strip())

            category = html.unescape(category)
            title = html.unescape(title)
            location = html.unescape(location)

            job_list.append({'category': category, 'title': title, 'location': location})

        return job_list
    else:
        print(f"Запрос не удался с кодом состояния {response.status_code}")
        return []


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["category", "title", "location"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)


# Получение данных о вакансиях
job_data = get_job_data()

# Сохранение данных в JSON
save_to_json(job_data, 'jobs.json')

# Сохранение данных в CSV
save_to_csv(job_data, 'jobs.csv')

# Вывод данных о вакансиях
print("Найденные вакансии:")
for job in job_data:
    print(job)
