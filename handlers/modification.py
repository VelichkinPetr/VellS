from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from buisness_logic.states import TestState, Testing
from buisness_logic.keyboards import create_keyboard
from buisness_logic.services.TestsDataService import TestsDataService
from handlers.testing import show_next_question

modification_router = Router()

@modification_router.callback_query(F.data.startswith("Subjects"))
async def choise_subs_callback_handler(callback: types.CallbackQuery, test_data_service: TestsDataService, state: FSMContext):
    await state.update_data(subject = callback.data)
    await state.set_state(TestState.chapter)

    sub_id = callback.data.split()[1]
    chapters = await test_data_service.get_chapters(int(sub_id))
    keyboard = create_keyboard(chapters, 'catalog')

    await callback.message.edit_text(text='Chapter choise', reply_markup=keyboard)

@modification_router.callback_query(F.data.startswith("Chapters"))
async def choise_chapters_callback_handler(callback: types.CallbackQuery, test_data_service: TestsDataService,  state: FSMContext):
    await state.update_data(chapter=callback.data)
    await state.set_state(TestState.topic)

    chapter_id = callback.data.split()[1]
    topics = await test_data_service.get_topics(int(chapter_id))
    data = await state.get_data()
    keyboard = create_keyboard(topics, data['subject'])

    await callback.message.edit_text(text='Topic choise',reply_markup=keyboard)

@modification_router.callback_query(F.data.startswith("Topics"))
async def choise_tests_callback_handler(callback: types.CallbackQuery, test_data_service: TestsDataService,  state: FSMContext):
    await state.update_data(topic=callback.data)

    topic_id = callback.data.split()[1]
    tests = await test_data_service.get_tests(int(topic_id))
    data = await state.get_data()
    keyboard = create_keyboard(tests, data['chapter'])

    await callback.message.edit_text(text='Test choise',reply_markup=keyboard)
    await state.set_state(TestState.test)

@modification_router.callback_query(F.data.startswith("Tests"))
async def question_callback_handler(callback: types.CallbackQuery,
                                    test_data_service: TestsDataService,
                                    state: FSMContext):
    await state.update_data(test=callback.data)
    test_id = callback.data.split()[1]
    questions = await test_data_service.get_questions(int(test_id))

    await state.update_data(questions=questions, index = 0, user_responses = '')

    await callback.answer()

    await show_next_question(callback,test_data_service, state)
    await state.set_state(Testing.answer)

