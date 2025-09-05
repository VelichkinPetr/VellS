from aiogram import Router, types, F
from aiogram.filters import command
from aiogram.fsm.context import FSMContext
from buisness_logic.services.TestsDataService import TestsDataService
from buisness_logic.keyboards import create_keyboard
from buisness_logic.states import TestState

start_router = Router()

@start_router.callback_query(F.data.startswith('catalog'))
@start_router.message(command.CommandStart())
async def start(update: types.Message | types.CallbackQuery, test_data_service: TestsDataService):
    subjects = await test_data_service.get_subjects()
    keyboard = create_keyboard(subjects, '')

    if isinstance(update, types.Message):
        await update.answer('Subjects choise',reply_markup=keyboard, cache_time=60)
    else:
        await update.message.edit_text(text='Subjects choise', reply_markup=keyboard)
