from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

def get_fresh_session_data(url):
    """Запускает headless браузер, загружает страницу и возвращает актуальные cookies и заголовки"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('-disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        time.sleep(5) # Как будто дичайший костыль?? Переделать под движок типа кода ниже

        # Явное ожидание загрузки страницы (можно настроить под нужный элемент)
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.TAG_NAME, 'body'))
        # )

        cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
        user_agent = driver.execute_script('return navigator.userAgent')

        headers = {
            'user-agent': user_agent,
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json'
        }

        return {
            'cookies': cookies,
            'headers': headers
        }

    finally:    
        driver.quit()

if __name__ == "__main__":
    target_url = "https://www.ozon.ru/"
    session_data = get_fresh_session_data(target_url)
    print(json.dumps(session_data, indent=2, ensure_ascii=False))