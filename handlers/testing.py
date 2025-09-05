from aiogram import Router, types
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext

from buisness_logic.states import Testing
from buisness_logic.services.TestsDataService import TestsDataService

testing_router = Router()

async def show_next_question(update: types.Message | types.CallbackQuery,
                             test_data_service: TestsDataService,
                             state: FSMContext):
    #получаем из state список вопросов и индекс вопроса
    data = await state.get_data()
    questions = data['questions']
    index = data['index']
    #фиксируем остановку цикла переборавопросов
    if index >= 3:
        data = await state.get_data()
        await update.answer(f'{data['user_responses'].split('|')}')
        return await update.answer(f'Тест окончен!!!')
    #получаем нужный вопрос
    question = questions[index]
    #получаем варианты ответов для этого вопроса
    answers = await test_data_service.get_answers(question.id)
    q_text = question.text.split('$')[0]#отделяем текст от ссылки на картинку
    path_png = question.text.split('$')[-1]
    #выбираем вариант вывода с картинкой и без
    if 'resources' in path_png:
        image_from_pc = FSInputFile(path_png)
        if isinstance(update, types.Message):
            await update.answer_photo(image_from_pc, caption=f'{q_text}\n{answers[0].text}')
        else:
            await update.message.answer_photo(image_from_pc, caption=f'{q_text}\n{answers[0].text}')
    else:
        if isinstance(update, types.Message):
            await update.answer(text=f'{q_text}\n{answers[0].text}')
        else:
            await update.message.answer(text=f'{q_text}\n{answers[0].text}')
    #сохраняем в state вопрос и правильный ответ
    await state.update_data(user_responses = data['user_responses'] + q_text + ' / ' + str(answers[0].is_correct) )
    # передвигаем указатель на следующий вопрос
    await state.update_data(index = index+1)

#поинт для состояния ввода ответа
@testing_router.message(Testing.answer)
async def answer_handler(message: types.Message,
                         test_data_service: TestsDataService,
                         state: FSMContext):
    #получаем вопрос и правильный ответ из state
    data = await state.get_data()
    #дописываем к ним то, что ответил пользователь
    await state.update_data(
        user_responses = data['user_responses'] + ' / '  + message.text+'|')
    # переходим к следующей итерации(вопросу)
    await show_next_question(message, test_data_service, state)