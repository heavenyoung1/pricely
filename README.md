# 📉 Pricely

Другие полезные методы:

`mock_method.assert_called()`          # Был ли вызван хотя бы раз

`mock_method.assert_called_with(args)` # Был ли вызван с конкретными аргументами (последний вызов)

`mock_method.assert_not_called()`      # НЕ был вызван

Обновления ORM моделей привели к этому:
```
# Быстрый доступ к текущей цене
product = session.get(ORMProduct, product_id)
current_price = product.current_price  # Через price_id

# История всех цен
all_prices = product.prices  # Через product_id в таблице prices

# В USE_CASE всё работает как задумано:
product.price_id = price_id  # ✅ Теперь это поле существует!
```