import json
from typing import Dict
from utils.logger import logger

class StateManager:
    def __init__(self, filename: str = "product_states.json"):
        '''Загружает состояния цен из файла'''
        self.filename = filename
        self.states: Dict[str, int] = self._load_states()

    def _load_states(self) -> Dict[str, int]:
        try:
            with open (self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.info('Файл состояний не найден, создание нового')
            return {}
        except json.JSONDecodeError:
            logger.warning('Ошибка декодирования JSON, возвращаем пустой словарь')
            return {}
        
    def save_states(self):
        '''Сохраняет состояния цен в файл'''
        try:
            with open (self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.states,f, ensure_ascii=False, indent=4)
            logger.info(f'Состояния сохранены в {self.filename}')
        except Exception as e:
            logger.error(f'Ошибка при сохранении состояний: {e}')

    def get_previous_price(self, url: str) -> int:
        '''Получает предыдущую цену по URL'''
        return self.states.get(url, 0)
    
    def update_price(self, url: str, price: int):
        '''Обновляет цену для URL'''
        self.states[url] = price
        self.save_states
    