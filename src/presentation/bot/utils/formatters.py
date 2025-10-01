def format_categories(categories) -> str:
    """Форматирует категории для красивого отображения"""
    if not categories:
        return "—"
    
    # Если это строка в формате {cat1,cat2,"cat3"}
    if isinstance(categories, str):
        if categories.startswith('{') and categories.endswith('}'):
            # Убираем фигурные скобки и разделяем по запятым
            categories_list = [cat.strip().strip('"') for cat in categories.strip('{}').split(',')]
            return ' → '.join(categories_list)
        else:
            return categories
    
    # Если это список или кортеж
    elif isinstance(categories, (list, tuple)):
        return " → ".join(str(cat) for cat in categories)
    
    # В остальных случаях просто возвращаем как строку
    return str(categories)

def format_product_message(product: dict) -> str:
    """
    Форматирует сообщение о товаре для Telegram (принимает словарь).
    """
    # Получаем последнюю цену из списка prices или из latest_price
    latest_price = None
    
    if "latest_price" in product and product["latest_price"]:
        latest_price = product["latest_price"]
    elif "prices" in product and product["prices"]:
        # Берем последний элемент из списка цен (самый новый)
        latest_price = product["prices"][-1]
        # Если это объект Price, преобразуем в словарь
        if hasattr(latest_price, '__dict__'):
            latest_price = {
                'with_card': latest_price.with_card,
                'without_card': latest_price.without_card,
                'created_at': latest_price.created_at
            }
    
    # Форматируем цены
    if latest_price:
        with_card = latest_price.get('with_card', '—')
        without_card = latest_price.get('without_card', '—')
        if with_card and with_card != '—':
            with_card = f"{with_card} ₽"
        if without_card and without_card != '—':
            without_card = f"{without_card} ₽"
    else:
        with_card = "—"
        without_card = "—"
    
    # Формируем сообщение
    text = (
        f"📦 {product.get('name', 'Неизвестный товар')}\n"
        f"💳 Цена с картой: {with_card}\n"
        f"💵 Цена без карты: {without_card}\n"
        f"🔗 <a href='{product.get('link', '#')}'>Ссылка на товар</a>"
    )
    
    return text