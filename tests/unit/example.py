# # Пример вызова
# if __name__ == "__main__":
#     parser = OzonParser()
#     ozon_url = "https://www.ozon.ru/product/dzhinsy-befree-883110146/"
#     product_data = parser.parse_product(ozon_url)
#     status_code = parser.get_page_status(ozon_url)
#     print(f"Название товара: {product_data['name']}")
#     print(f"ID товара: {product_data['id']}")
#     print(f"Рейтинг товара: {product_data['rating']}")
#     print(f"Цена товара с картой: {product_data['price_with_card']}")
#     print(f"Цена товара без карты: {product_data['price_without_card']}")
#     print(f"Цена товара дефолт: {product_data['price_default']}")
#     print(f"Изображение товара: {product_data['image_url']}")
#     print(f"Категории товара: {product_data['categories']}")
#     print(f'СТАТУС HTTP -> {status_code}')