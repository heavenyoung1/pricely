from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from src.presentation.bot.utils.fsm import ProductAddState
from src.infrastructure.services import product_service
from src.infrastructure.services import logger
from src.presentation.bot.utils.formatters import format_product_message, format_categories
from src.presentation.bot.utils.keyboard import build_product_actions_keyboard

# ================= ДОБАВИТЬ ТОВАР ================= #

# 1️⃣ Обработчик команды "➕ Добавить товар"
async def add_product_request(message: Message, state: FSMContext):
    '''
    Обработчик команды "/add_product".

    Этот метод срабатывает при получении команды "/add_product" от пользователя и выполняет следующие действия:
    - Отправляет пользователю сообщение с просьбой отправить ссылку на товар.
    - Устанавливает состояние FSM в "waiting_for_url", чтобы ожидать от пользователя URL товара.
    - Информирует пользователя о начале процесса парсинга товара.

    Аргументы:
    - message (Message): Сообщение от пользователя, содержащее команду "/add_product".
    - state (FSMContext): Контекст состояния FSM, используемый для управления состоянием бота в диалоге с пользователем.
    '''
    await message.answer("📦 Отправь ссылку на товар с Ozon")
    # Устанавливаем состояние ожидания URL товара (если используем FSM, можно это добавить в следующий шаг)
    await state.set_state(ProductAddState.waiting_for_url)
    # Переход в следующее состояние, где пользователь отправит URL товара
    await message.answer("⏳ Парсинг начался, ожидайте...")

async def add_product_process(message: Message, state: FSMContext):
    '''
    Обработчик получения URL товара и добавления товара в систему.

    Этот метод срабатывает, когда пользователь отправляет URL товара в ответ на запрос бота (после команды "/add_product").
    Он выполняет следующие действия:
    - Проверяет, находится ли пользователь в нужном состоянии (ожидание URL товара).
    - Парсит URL и пытается добавить товар в систему через вызов метода create_product.
    - Отправляет пользователю сообщение с результатом добавления товара: название товара, цена с картой и без.
    - В случае ошибки отправляется сообщение с описанием проблемы.
    - Очищает состояние FSM после завершения добавления товара.

    Аргументы:
    - message (Message): Сообщение от пользователя, содержащее URL товара.
    - state (FSMContext): Контекст состояния FSM, который используется для проверки текущего состояния и управления состоянием бота.
    '''
    if not await state.get_state() == ProductAddState.waiting_for_url:
        return  # Игнорируем, если пользователь не в этом состоянии
    
    url = message.text.strip()
    try:
        result = product_service.create_product(str(message.from_user.id), url)
        await message.answer(
            f"✅ Товар добавлен!\n\n"
            f"Название: {result['product_name']}\n"
            f"Цена с картой: {result['with_card']} ₽\n"
            f"Цена без карты: {result['without_card']} ₽",
            reply_markup=build_product_actions_keyboard(result['product_id'], result['link'])
        )
    except Exception as e:
        logger.exception("Ошибка при добавлении товара")
        await message.answer(f"❌ Ошибка: {e}")

    # Сбрасываем состояние
    await state.clear()

# ================= ПОЛУЧИТЬ СПИСОК ТОВАРОВ ================= #

async def get_my_product_list(message: Message):
    '''
    Обработчик команды для получения списка товаров пользователя.

    Этот метод срабатывает, когда пользователь вызывает команду для получения списка своих товаров.
    Он выполняет следующие действия:
    - Получает все товары пользователя через `product_service.get_all_products()`.
    - Если товаров нет, отправляет сообщение, что у пользователя нет отслеживаемых товаров.
    - Если товары есть, формирует клавиатуру с кнопками для каждого товара и отправляет её пользователю.

    Аргументы:
    - message (Message): Сообщение от пользователя, содержащее запрос на получение списка товаров.

    Исключения:
    - В случае ошибки при получении списка товаров или других непредвиденных ошибок, ошибка будет залогирована,
      и пользователю отправится сообщение с описанием ошибки.    
    '''
    try:
        # Получаем список товаров пользователя
        products = product_service.get_all_products(str(message.from_user.id))
        # Если товаров нет
        if not products:
            await message.answer('📭 У вас пока нет отслеживаемых товаров')
            return
        
        inline_keyboard = []  # Список для хранения рядов кнопок

        # Создаем отдельный ряд для каждой кнопки
        for p in products: 
            name = p.get('name') or p.get('product_name') or p.get('id')
            display = name if len(name) <= 60 else name[:57] + '...'
            # Каждая кнопка в отдельном списке = отдельный ряд
            inline_keyboard.append([InlineKeyboardButton(text=display, callback_data=f"product:{p['id']}")])

        # Создаем клавиатуру с кнопками (каждая в отдельном ряду)
        kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        
        # Отправляем сообщение с клавиатурой
        await message.answer("📋 Ваши товары:", reply_markup=kb)

    except Exception as e:
        logger.exception('Ошибка при получении списка товаров')
        await message.answer(f'❌ Ошибка: {e}')
        
async def handle_product_button(call: CallbackQuery):
    '''
    Обработчик нажатия на кнопку товара.

    Этот метод срабатывает при нажатии на кнопку с товаром в списке.
    Он выполняет следующие действия:
    - Отправляет ответ на callback, чтобы избежать "залипания" кнопки.
    - Извлекает ID товара из callback_data и получает полную информацию о товаре через `product_service.get_full_product()`.
    - Если товар найден, формирует сообщение с подробной информацией о товаре и отправляет его пользователю.
    - Если товар не найден, отправляется сообщение об ошибке.
    
    Аргументы:
    - call (CallbackQuery): Данные callback-запроса, содержащие информацию о нажатой кнопке и ID товара.

    Исключения:
    - В случае ошибки при извлечении данных товара или других непредвиденных ошибок, ошибка будет залогирована,
      и пользователю отправится сообщение с описанием ошибки.
    '''
    await call.answer() # Отправляем ответ на callback, чтобы избежать 'залипания' кнопки
    
    # Извлекаем ID продукта из callback_data
    product_id = call.data.split(':', 1)[1]

    try:
        # Получаем полный продукт
        product = product_service.get_full_product(product_id)
        if not product:
            await call.message.edit_text('❌ Товар не найден.')
            return
        
        text = format_product_message(product)
         # Создаем клавиатуру для действия с продуктом
        kb = build_product_actions_keyboard(product_id=product['id'], product_link=product['link'])

        # Редактируем сообщение с информацией о товаре
        await call.message.edit_text(
            text=text,
            parse_mode='HTML',
            reply_markup=kb,
            disable_web_page_preview=False
        )

    except Exception as e:
        logger.exception('Ошибка в handle_product_button')
        await call.answer(f'Ошибка: {e}')

# 3️⃣ Обновить цену
async def handle_update_price(call: CallbackQuery):
    '''
    Обработчик обновления цены товара.

    Этот метод срабатывает при нажатии на кнопку "Обновить цену" для товара.
    Он выполняет следующие действия:
    - Отправляет ответ на callback-запрос, чтобы избежать задержек или "залипания" кнопки.
    - Извлекает ID товара из callback_data и вызывает сервис для обновления цены товара.
    - Если обновление прошло успешно, формирует новое сообщение с актуальной информацией о товаре и обновленной клавиатурой.
    - Если данные не изменились, обновление сообщения не требуется.
    - В случае ошибки при обновлении цены или при обработке сообщения, ошибка логируется, и пользователю отправляется сообщение с описанием ошибки.

    Аргументы:
    - call (CallbackQuery): Данные callback-запроса, содержащие информацию о нажатой кнопке и ID товара.

    Исключения:
    - В случае ошибки при обновлении цены или редактировании сообщения, ошибка будет залогирована,
      и пользователю будет отправлено сообщение об ошибке с кнопкой "Назад", чтобы вернуться к товару.
    '''
    product_id = call.data.split(':', 1)[1]
    logger.debug(f'В кнопке получен {product_id}')
    logger.info(f'Начинаем обновление цены для товара {product_id}')

    # # Сразу отвечаем на callback, чтобы избежать timeout
    # try:
    #     await call.answer('🔄 Обновляем цену...')
    # except Exception as e:
    #     logger.warning(f'Не удалось ответить на callback query: {e}')

    try:
        # Обновляем цену
        logger.info('Вызываем service.update_product_price')
        updated_product = product_service.update_product_price(product_id)
        logger.info(f'Получили обновленный товар: {type(updated_product)} - {updated_product}')

        # Формируем новое сообщение
        logger.info('Формируем новое сообщение')
        # УБРАЛИ AWAIT так как фукнция синхронная
        new_text = format_product_message(updated_product)
        logger.info(f'Сформированный текст: {new_text}')

        new_markup = build_product_actions_keyboard(product_id, updated_product['link'])
        logger.info('Клавиатура сформирована')

        # Проверка на изменения, чтобы избежать отправки одинаковых данных
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        current_text = call.message.text
        current_markup = call.message.reply_markup

        if new_text != current_text or new_markup != current_markup:
            logger.info('Обновляем сообщение с новыми данными')
            await call.message.edit_text(
                text=new_text,
                parse_mode='HTML',
                reply_markup=new_markup,
                disable_web_page_preview=False
            )
            logger.info('✅ Сообщение успешно обновлено!')
        else:
            logger.info('Данные не изменились, обновление не требуется.')
        
    except Exception as e:
        logger.exception('❌ Ошибка при обновлении цены')
        
        # В случае ошибки показываем сообщение об ошибке
        try:
            kb = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='🔙 Назад', callback_data=f'product:{product_id}')]
                ]
            )

            await call.message.edit_text(
                f'❌ Ошибка при обновлении цены: {e}',
                reply_markup=kb
            )
        except Exception as edit_error:
                logger.exception('Не удалось обновить сообщение с ошибкой')   

    