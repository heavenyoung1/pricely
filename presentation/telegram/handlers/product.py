from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from infrastructure.database.unit_of_work import UnitOfWorkFactory
from infrastructure.parsers.browser import BrowserManager
from infrastructure.parsers.parser import ProductParser
from domain.entities.product_fields import ProductFieldsForAdd, ProductFieldsForCheck
from application.use_cases.add_product import AddProductUseCase
from application.use_cases.get_user_products import GetUserProductsUseCase
from application.use_cases.get_product import GetProductUseCase
from application.use_cases.remove_product import RemoveProductUseCase
from domain.exceptions import ProductAlreadyExistsError, ProductNotFoundError
from presentation.telegram.keyboards.inline import (
    product_list,
    product_detail,
    confirm_delete,
    cancel,
)
from presentation.telegram.keyboards.reply import (
    main_menu,
    BTN_ADD_PRODUCT,
    BTN_MY_PRODUCTS,
)
from core.logger import logger

router = Router()


class AddProductState(StatesGroup):
    waiting_for_url = State()


@router.message(F.text == BTN_ADD_PRODUCT)
async def add_product_start(message: Message, state: FSMContext):
    '''Начало добавления товара'''
    await message.answer(
        'Отправь ссылку на товар:',
        reply_markup=cancel(),
    )
    await state.set_state(AddProductState.waiting_for_url)


@router.message(AddProductState.waiting_for_url)
async def add_product_url(
    message: Message,
    state: FSMContext,
    uow_factory: UnitOfWorkFactory,
):
    '''Обработка URL товара'''
    url = message.text.strip()

    # Валидация URL
    if not url.startswith('http'):
        await message.answer(
            'Некорректная ссылка. Отправь ссылку, начинающуюся с http:',
            reply_markup=cancel(),
        )
        return

    await message.answer('⏳ Добавляю товар, ожидайте...')

    try:
        # Получаем user_id
        chat_id = str(message.chat.id)
        async with uow_factory.create() as uow:
            user = await uow.user_repo.get_by_chat_id(chat_id)
            if not user:
                await message.answer('Ошибка: пользователь не найден. Напиши /start')
                await state.clear()
                return
            user_id = user.id

        # Парсим и добавляем товар
        async with BrowserManager() as browser:
            parser = ProductParser(
                browser=browser,
                fields_for_add=ProductFieldsForAdd(),
                fields_for_check=ProductFieldsForCheck(),
            )
            add_product = AddProductUseCase(
                parser=parser,
                uow_factory=uow_factory,
            )
            product = await add_product.execute(
                url=url,
                user_id=user_id,
                change=5,
            )

        await message.answer(
            f'✅ Товар добавлен!\n\n'
            f'<b>{product.name}</b>\n'
            f'💳 <b>Цена с картой</b: {product.price_with_card} ',
            reply_markup=main_menu(),
        )

    except ProductAlreadyExistsError:
        await message.answer(
            '❗ Этот товар уже отслеживается.',
            reply_markup=main_menu(),
        )
    except Exception as e:
        logger.error(f'Ошибка добавления товара: {e}')
        await message.answer(
            'Не удалось добавить товар. Проверь ссылку и попробуй снова.',
            reply_markup=main_menu(),
        )

    await state.clear()


@router.message(F.text == BTN_MY_PRODUCTS)
async def my_products(message: Message, uow_factory: UnitOfWorkFactory):
    '''Список товаров пользователя'''
    chat_id = str(message.chat.id)

    async with uow_factory.create() as uow:
        user = await uow.user_repo.get_by_chat_id(chat_id)
        if not user:
            await message.answer(
                'Ошибка: пользователь не найден. Напиши /start',
            )
            return

    get_products = GetUserProductsUseCase(uow_factory)
    products = await get_products.execute(user.id)

    if not products:
        await message.answer(
            '📭 У тебя пока нет отслеживаемых товаров.',
        )
    else:
        await message.answer(
            f'Твои товары:',
            reply_markup=product_list(products),
        )


@router.callback_query(F.data.startswith('product:'))
async def show_product(callback: CallbackQuery, uow_factory: UnitOfWorkFactory):
    '''Показать детали товара'''
    product_id = int(callback.data.split(':')[1])

    try:
        get_product = GetProductUseCase(uow_factory)
        product = await get_product.execute(product_id)

        text = (
            f'<b>{product.name}</b>\n\n'
            f'Артикул: {product.article}\n'
            f'Цена с картой: {product.price_with_card} ₽\n'
            f'Цена без карты: {product.price_without_card} ₽\n'
            f'Порог уведомления: {product.change}%\n'
            f'{product.link}'
        )

        await callback.message.edit_text(
            text,
            reply_markup=product_detail(product_id),
        )

    except ProductNotFoundError:
        await callback.message.delete()
        await callback.message.answer('Товар не найден.')

    await callback.answer()


@router.callback_query(F.data == 'my_products')
async def my_products_callback(callback: CallbackQuery, uow_factory: UnitOfWorkFactory):
    '''Возврат к списку товаров (из inline кнопок)'''
    chat_id = str(callback.message.chat.id)

    async with uow_factory.create() as uow:
        user = await uow.user_repo.get_by_chat_id(chat_id)
        if not user:
            await callback.message.edit_text(
                'Ошибка: пользователь не найден. Напиши /start'
            )
            await callback.answer()
            return

    get_products = GetUserProductsUseCase(uow_factory)
    products = await get_products.execute(user.id)

    if not products:
        await callback.message.edit_text('У тебя пока нет отслеживаемых товаров.')
    else:
        await callback.message.edit_text(
            f'Твои товары ({len(products)}):',
            reply_markup=product_list(products),
        )

    await callback.answer()


@router.callback_query(F.data.startswith('delete:'))
async def delete_product_confirm(callback: CallbackQuery):
    '''Подтверждение удаления'''
    product_id = int(callback.data.split(':')[1])

    await callback.message.edit_text(
        'Удалить товар из отслеживания?',
        reply_markup=confirm_delete(product_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith('confirm_delete:'))
async def delete_product(callback: CallbackQuery, uow_factory: UnitOfWorkFactory):
    '''Удаление товара'''
    product_id = int(callback.data.split(':')[1])

    try:
        remove_product = RemoveProductUseCase(uow_factory)
        await remove_product.execute(product_id)

        await callback.message.delete()
        await callback.message.answer('Товар удалён.')

    except ProductNotFoundError:
        await callback.message.delete()
        await callback.message.answer('Товар не найден.')

    await callback.answer()
