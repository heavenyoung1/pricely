import random 
import json
import logging
from .user_agents import user_agents_list as user_agents

logger = logging.getLogger(__name__)

def _get_user_agent():
    try:
        index = random.randrange(len(user_agents))
        user_agent = user_agents[index]
        logger.info(f'UserAgent успешно получен {user_agent}')
        return user_agent
    except Exception as e:
        logger.error(f'Ошибка получения UserAgent: {e}')
        raise

# Загрузка прокси из файла
def _load_proxies():
    try:
        with open('src/infrastructure/parsers/utils/proxy.json', 'r', encoding='utf-8') as file:
            proxies = json.load(file)
        return proxies
    except Exception as e:
        logger.error(f'Ошибка считывания Прокси: {e}')
        raise


def _get_proxy():
    try:
        proxies = _load_proxies()
        proxy_data = random.choice(proxies)
        proxy = proxy_data['proxy']
        user = proxy_data['user']
        password = proxy_data['password']

        return proxy, user, password
    except Exception as e:
        logger.error(f'Ошибка получения Прокси: {e}')
        raise