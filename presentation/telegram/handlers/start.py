from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from infrastructure.database.unit_of_work import UnitOfWorkFactory
from application.use_cases.create_user import CreateUserUseCase
from domain.entities.user import User
from presentation.telegram.keyboards.inline import main_menu
from core.logger import logger

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, uow_factory: UnitOfWorkFactory):
    '''Обработчик команды /start'''
    chat_id = str(message.chat.id)
    username = message.from_user.username or message.from_user.first_name

    # Проверяем/создаём пользователя
    async with uow_factory.create() as uow:
        existing_user = await uow.user_repo.get_by_chat_id(chat_id)

        if not existing_user:
            create_user = CreateUserUseCase(uow_factory)
            user = User.create(username=username, chat_id=chat_id)
            await create_user.execute(user)
            logger.info(f'Создан новый пользователь: {username} ({chat_id})')

    await message.answer(
        f'Привет, <b>{username}</b>!\n\n'
        'Я помогу отслеживать цены на товары.\n'
        'Выбери действие:',
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback: CallbackQuery):
    '''Возврат в главное меню'''
    await callback.message.edit_text(
        'Выбери действие:',
        reply_markup=main_menu(),
    )
    await callback.answer()
