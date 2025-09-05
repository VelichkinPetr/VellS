import asyncio
import os

import dotenv

from buisness_logic.bot import create
from handlers.start import start_router
from handlers.modification import modification_router
from handlers.testing import testing_router

from buisness_logic.services.subjects_service import SubjectsService
from buisness_logic.services.charapters_service import ChaptersService
from buisness_logic.services.topics_service import TopicsService
from buisness_logic.services.tests_service import TestsService
from buisness_logic.services.questions_service import QuestionsService
from buisness_logic.services.answers_service import AnswersService
from buisness_logic.services.TestsDataService import TestsDataService

from buisness_logic.repo.subjects_repo import SubjectsRepo
from buisness_logic.repo.chapters_repo import ChaptersRepo
from buisness_logic.repo.topics_repo import TopicsRepo
from buisness_logic.repo.test_repo import TestsRepo
from buisness_logic.repo.questions_repo import QuestionsRepo
from buisness_logic.repo.answers_repo import AnswersRepo

from middlewares.session import TestDataServiceMiddleware, TestDataServiceMiddlewareCallback

async def main():
    dotenv.load_dotenv()
    db_path = os.getenv('PATH_DB')

    SUBJECTS_SERV = SubjectsService(SubjectsRepo(db_path))
    CHAPTERS_SERV = ChaptersService(ChaptersRepo(db_path))
    TOPICS_SERV = TopicsService(TopicsRepo(db_path))
    TESTS_SERV = TestsService(TestsRepo(db_path))
    QUESTIONS_SERV = QuestionsService(QuestionsRepo(db_path))
    ANSWERS_SERV = AnswersService(AnswersRepo(db_path))

    test_data_serv = TestsDataService([SUBJECTS_SERV, CHAPTERS_SERV, TOPICS_SERV, TESTS_SERV, QUESTIONS_SERV, ANSWERS_SERV])
    bot, dp = create()
    dp.include_routers(start_router, modification_router, testing_router)
    dp.message.middleware(TestDataServiceMiddleware(test_data_serv))
    dp.callback_query.middleware(TestDataServiceMiddlewareCallback(test_data_serv))

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


