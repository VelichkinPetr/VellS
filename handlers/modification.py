from aiogram import Router, types, F
from aiogram.filters import command
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


modification_router = Router()


@modification_router.message(command.Command('add_book','a'))
async def add_book(message: types.Message):

    args = message.text.split()[1:]
    user_id = message.from_user.id

    try:
        await BookService().add_book(user_id, args)
        await message.answer(f'Mission completed! Book add!')

    except ValueError:
        await message.answer("Oops! Usage: /add_book of /a 'title' 'pages_count'")

    except TypeError:
        await message.answer("Oops! need is digit => 'pages_count'")

    except KeyError:
        await message.answer("Sorry Book in Base =)")
