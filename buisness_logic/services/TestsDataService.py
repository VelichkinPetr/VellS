from __future__ import annotations
import os
import asyncio
import dotenv
from sqlite3 import IntegrityError
from buisness_logic.db import Subjects

from buisness_logic.services.subjects_service import SubjectsService
from buisness_logic.services.topics_service import TopicsService
from buisness_logic.services.tests_service import TestsService
from buisness_logic.services.questions_service import QuestionsService
from buisness_logic.services.answers_service import AnswersService

from buisness_logic.repo.subjects_repo import SubjectsRepo
from buisness_logic.repo.topics_repo import TopicsRepo
from buisness_logic.repo.test_repo import TestsRepo
from buisness_logic.repo.questions_repo import QuestionsRepo
from buisness_logic.repo.answers_repo import AnswersRepo

class TestsDataService:

    def __init__(self, services: list[SubjectsService, TopicsService, TestsService, QuestionsService, AnswersService]):
        self.subs_s, self.topics_s, self.tests_s, self.quest_s, self.answer_s = services

    async def add_test(self, sub_name: str, description: str,
                       topic_text: str,
                       test_num: int,
                       quest_text: str,
                       answers: str, is_correct: int) -> None:

        await self.subs_s.add_subject(sub_name, description)
        await self.topics_s.add_topic(sub_name, topic_text)
        topic_id = await self.topics_s.find_id(sub_name, topic_text)

        await self.tests_s.add_test(topic_id, test_num)
        test_id = await self.tests_s.find_id(topic_id, test_num)

        await self.quest_s.add_question(test_id, quest_text)
        quest_id = await self.quest_s.find_id(test_id, quest_text)

        await self.answer_s.add_answer(quest_id, answers, is_correct)

    async def get_tests(self, topic_id: int):
        return await self.tests_s.list_tests(topic_id)

    async def get_questions(self, test_id: int):
        return await self.quest_s.list_questions(test_id)




async def main():
    dotenv.load_dotenv()
    db_path = os.getenv('PATH_DB')

    SUBJECTS_SERV = SubjectsService(SubjectsRepo(db_path))
    TOPICS_REPO = TopicsService(TopicsRepo(db_path))
    TESTS_REPO = TestsService(TestsRepo(db_path))
    QUESTIONS_REPO = QuestionsService(QuestionsRepo(db_path))
    ANSWERS_REPO = AnswersService(AnswersRepo(db_path))
    await QUESTIONS_REPO.remove_question(1,2)
    print(await QUESTIONS_REPO.find_id(1, 'выбери от 1 до 5'))
    t = TestsDataService([SUBJECTS_SERV, TOPICS_REPO, TESTS_REPO, QUESTIONS_REPO, ANSWERS_REPO])
    await t.add_test('Биология', 'щпимание', 'Организм', 1, 'Вопрос 1', '1,2,3,4', 3)

    print(await t.get_tests(1))
    print(await t.get_questions(1))


if __name__ == '__main__':
    asyncio.run(main())