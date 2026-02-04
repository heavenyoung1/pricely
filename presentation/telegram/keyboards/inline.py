from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List

from domain.entities.product import Product


def product_list(products: List[Product]) -> InlineKeyboardMarkup:
    '''Список товаров пользователя'''
    builder = InlineKeyboardBuilder()
    for product in products:
        builder.row(
            InlineKeyboardButton(
                text=(
                    f'{product.name[:30]}...'
                    if len(product.name) > 30
                    else product.name
                ),
                callback_data=f'product:{product.id}',
            )
        )
    builder.row(
        InlineKeyboardButton(text='« Назад', callback_data='back_to_menu'),
    )
    return builder.as_markup()


def product_detail(product_id: int) -> InlineKeyboardMarkup:
    '''Детали товара'''
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Удалить', callback_data=f'delete:{product_id}'),
    )
    builder.row(
        InlineKeyboardButton(text='« К списку', callback_data='my_products'),
    )
    return builder.as_markup()


def confirm_delete(product_id: int) -> InlineKeyboardMarkup:
    '''Подтверждение удаления'''
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='✅ Да, удалить', callback_data=f'confirm_delete:{product_id}'
        ),
        InlineKeyboardButton(text='❌ Отмена', callback_data=f'product:{product_id}'),
    )
    return builder.as_markup()


def cancel() -> InlineKeyboardMarkup:
    '''Кнопка отмены'''
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='❌ Отмена', callback_data='back_to_menu'),
    )
    return builder.as_markup()
