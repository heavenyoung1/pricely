import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
from utils.webdriver import init_driver
import cloudscraper
import time
import random
import cloudscraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import json
from utils.logger import logger

class OzonEngine:
    def __init__(self, headless=True, user_agent=None, proxy=None):
        self.driver = init_driver(headless, user_agent, proxy)
        self.scraper = cloudscraper.create_scraper() # Для API - запросов
        self.cookies = {}
        self.headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'user-agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        }
    
    def get_fresh_session_data(self, url='https://www.ozon.ru/'):
        """Загружает страницу и возвращает актуальные cookies и заголовки"""
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
        # Попытка принять cookies, если есть кнопка
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))).click()
            logger.info("Cookies приняты")
        except Exception as e:
            logger.info('Кнопка принятия cookies не найдена')

        # Синхронизируем cookies с драйвером
        self.cookies = {cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()}
        self.headers['user-agent'] = self.driver.execute_script('return navigator.userAgent')
        logger.info(f'Получены cookies: {self.cookies}')
        logger.info(f'Обновлены заголовки: {self.headers}')

        # Синхронизируем cookie с драйвером
        self.driver.delete_all_cookies()
        for name, value in self.cookies.items():
            self.driver.add_cookie({
                'name': name,
                'value': value,
                'domain': 'ozon.ru',
                'path': '/',
            })

            return {'cookies': self.cookies, 'headers': self.headers}
