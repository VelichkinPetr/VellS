from aiogram import Router,types
from aiogram.filters import command

start_router = Router()


@start_router.message(command.CommandStart())
async def start(message: types.Message):

    book_repo = BookRepo("database.db")
    user_stats_repo = UserStatsRepo("database.db")

    await user_stats_repo.init_tables()
    await user_stats_repo.create_stats(message.from_user.id)

    await book_repo.init_tables()
    await message.answer(f'«BookTracker» — бот для учёта чтения книг.\n'
                         f'С его помощью пользователь может:\n'
                         f'/add_book or /a <title> - Добавить книгу в список чтения.\n'
                         f'/mark_read or /m <id> <pages> - Отметить прочитанные страницы.\n'
                         f'/list_books or /l - Просмотреть список своих книг и прогресс по каждой из них.\n'
                         f'/remove_book or /r <book_id> - Удалить книгу из учёта.')
