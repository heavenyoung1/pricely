import cloudscraper
import http.client as http_client
from utils.logger import logger
from utils.cookies import get_fresh_session_data
import json
http_client.HTTPConnection.debuglevel = 1

scraper = cloudscraper.create_scraper()

def make_request(url, session_data, params=None):
    response = scraper.get(url, params=params, cookies=session_data['cookies'], headers=session_data['headers'])

    if response.status_code == 200:
        return response.text
    # else:
    #     response.raise_for_status()


if __name__ == "__main__":
    target_url = "https://www.ozon.ru/"

    # Получаем актуальные cookies и headers
    session_data = get_fresh_session_data(target_url)
    print(json.dumps(session_data, indent=2, ensure_ascii=False))

    # Пример парсинга другой страницы с полученными cookies и headers
    parse_url = "https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=/category/igrushki-9048/"
    html = make_request(parse_url, session_data)

    print(html)  # Выводим первые 1000 символов ответа