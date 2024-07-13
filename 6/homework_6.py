import requests
from bs4 import BeautifulSoup
import json


def get_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.text


def parse_bbc_news():
    url = 'https://www.bbc.com/sport'
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    news_links = []

    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/sport/' in href and 'articles' in href:
            full_link = 'https://www.bbc.com' + href.split('#')[0]
            if full_link not in news_links:
                news_links.append(full_link)

    return news_links[:5]


def parse_article_details(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')

    title = soup.find('h1').get_text(strip=True)

    related_topics = []
    related_topics_section = soup.find('div', class_='ssrcss-17ehax8-Cluster e1ihwmse1')
    if related_topics_section:
        for topic in related_topics_section.find_all('a', class_='ssrcss-1ef12hb-StyledLink ed0g1kj0'):
            related_topics.append(topic.get_text(strip=True))

    return title, related_topics


def main():
    news_links = parse_bbc_news()
    news_data = []

    for index, link in enumerate(news_links, start=1):
        title, related_topics = parse_article_details(link)
        news_item = {
            'Title': title,
            'Link': link,
            'Related Topics': related_topics
        }
        news_data.append(news_item)
        print(f"Article {index}: {title}")
        print(f"Link: {link}")
        print(f"Related Topics: {', '.join(related_topics) if related_topics else 'None'}\n")

    with open('news_topics.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
