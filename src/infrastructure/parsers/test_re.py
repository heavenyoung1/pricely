import re

def is_url(text):
    """Проверяет, начинается ли строка с https://"""
    pattern = r'^https?://'
    return bool(re.match(pattern, text))

def exctract_link(input_element: str) -> str:
    '''
    Проверяет, является ли переданный текст ссылкой на Ozon. Если это не ссылка,
    извлекает ссылку из текста.
    
    :param input_str: Строка, которая может быть ссылкой или содержать ссылку.
    :return: Ссылка на товар на Ozon.
    :raises ValueError: Если в строке не найдено валидной ссылки на Ozon.
    '''
    if is_url(input_element):
        return input_element 
    else:
        print('HERE')
        listing = input_element.split()
        url = listing[-1]
        return url

print(exctract_link('https://ozon.ru/t/UL6IfTg'))
print(exctract_link('erferge wefwef wef ewrf wedf we https://ozon.ru/t/UL6IfTg'))
print(exctract_link('https://www.ozon.ru/product/krossovki-adidas-sportswear-lite-racer-adapt-5-0-1351993979/?at=nRtrvLKOVfMzppQnt41mokBiWwyVNAFDloYlWUXqp0Np'))

