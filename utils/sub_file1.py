from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

def get_fresh_cookies_and_headers(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('-disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(5)    # Дать странице полностью загрузиться, можно заменить на явное ожидание

    cookies = driver.get_cookies()

    cookie_dict = {}
    for cookie in cookies:
        #cookie_dict[cookie.name] = cookie.value # Какой из двух вариантов лучшк и какой работает??
        cookie_dict[cookie['name']] = cookie['value']

    headers = {
        'user-agent': driver.execute_script('return navigator.userAgent')
    }

    driver.quit()

    return cookie_dict, headers

if __name__ == "__main__":
    target_url = "https://www.ozon.ru/"
    cookies, headers = get_fresh_cookies_and_headers(target_url)

    print(json.dumps({"cookies": cookies, "headers": headers}, indent=2, ensure_ascii=False))