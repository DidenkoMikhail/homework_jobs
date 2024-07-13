import requests
import re
import json
import sqlite3


def fetch_page_content(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Запрос не удался с кодом состояния {response.status_code}")
        return ""


def extract_jobs_from_content(content: str) -> list:
    job_pattern = re.compile(r'<h3 class="jobCard_title">(.*?)</h3>.*?href="(.*?)"', re.DOTALL)
    jobs = []

    matches = job_pattern.findall(content)
    for match in matches:
        title = match[0].strip()
        url = 'https://www.lejobadequat.com' + match[1].strip()
        jobs.append({'title': title, 'url': url})

    return jobs


def save_to_json(jobs: list, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, ensure_ascii=False, indent=4)
    print(f"Результаты успешно сохранены в файле {filename}")


def save_to_sqlite(jobs: list, db_name: str) -> None:
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, url TEXT)''')

    for job in jobs:
        c.execute('INSERT INTO jobs (title, url) VALUES (?, ?)', (job['title'], job['url']))

    conn.commit()
    conn.close()
    print(f"Результаты успешно сохранены в базе данных {db_name}")


def main() -> None:
    base_url = "https://www.lejobadequat.com/emplois"
    jobs = []

    for page in range(1, 3):  # Парсим первые две страницы
        url = f"{base_url}?page={page}"
        content = fetch_page_content(url)
        if content:
            jobs.extend(extract_jobs_from_content(content))

    for i, job in enumerate(jobs, 1):
        job['id'] = i

    save_to_json(jobs, 'jobs.json')
    save_to_sqlite(jobs, 'jobs.db')


if __name__ == "__main__":
    main()
