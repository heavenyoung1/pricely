from utils.webdriver import init_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_driver = init_driver()
url = 'https://www.ozon.ru/product/lanch-boks-850-ml-konteyner-dlya-hraneniya-edy-s-otdeleniyami-i-priborami-1549274404/'
base_driver.get(url)

name = WebDriverWait(base_driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.mp9_27.tsHeadline550Medium'))
).text

price_obj = WebDriverWait(base_driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.m8o_27.om6_27'))
).text
price = price_obj.split()[0].strip()

articule_obj = WebDriverWait(base_driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Артикул')]"))
).text
articule = articule_obj.split()[-1].strip()

image = WebDriverWait(base_driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'img[elementtiming^="lcp_eltiming_webGallery"]'))
)
score_obj = WebDriverWait(base_driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'отзыв')]"))
).text
rating = score_obj.split('•')[0].strip()

print('-----------')
print(url)
print("Название:", name)
print("Артикул:", articule)
print("Цена:", price)
print("Рейтинг:", rating)
print("Изображение:", image.get_attribute("src"))
print('-----------')

