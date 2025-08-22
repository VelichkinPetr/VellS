from __future__ import annotations
import os
import asyncio
import dotenv

from buisness_logic.services.subjects_service import SubjectsService
from buisness_logic.services.charapters_service import ChaptersService
from buisness_logic.services.topics_service import TopicsService
from buisness_logic.services.tests_service import TestsService
from buisness_logic.services.questions_service import QuestionsService
from buisness_logic.services.answers_service import AnswersService

from buisness_logic.repo.subjects_repo import SubjectsRepo
from buisness_logic.repo.chapters_repo import ChaptersRepo
from buisness_logic.repo.topics_repo import TopicsRepo
from buisness_logic.repo.test_repo import TestsRepo
from buisness_logic.repo.questions_repo import QuestionsRepo
from buisness_logic.repo.answers_repo import AnswersRepo

class TestsDataService:

    def __init__(self, services: list[SubjectsService,ChaptersService, TopicsService, TestsService, QuestionsService, AnswersService]):
        self.subs_s, self.chapter_s, self.topics_s, self.tests_s, self.quest_s, self.answer_s = services

    async def add_test(self, sub_name: str, description: str,
                       chapter_name: str,
                       topic_name: str,
                       test_num: int,
                       quest_text: str,
                       answers: str, is_correct: int) -> None:

        await self.subs_s.add_subject(sub_name, description)
        sub_id = await self.subs_s.find_id(sub_name)

        await self.chapter_s.add_chapter(sub_id, chapter_name)
        chapter_id = await self.chapter_s.find_id(sub_id,chapter_name)

        await self.topics_s.add_topic(chapter_id, topic_name)
        topic_id = await self.topics_s.find_id(chapter_id, topic_name)

        await self.tests_s.add_test(topic_id, test_num)
        test_id = await self.tests_s.find_id(topic_id, test_num)

        await self.quest_s.add_question(test_id, quest_text)
        quest_id = await self.quest_s.find_id(test_id, quest_text)

        await self.answer_s.add_answer(quest_id, answers, is_correct)

    async def get_subjects(self):
        return await self.subs_s.list_subjects()

    async def get_chapters(self, sub_id: int):
        return await self.chapter_s.list_chapters(sub_id)

    async def get_topics(self, chapter_id: int):
        return await self.topics_s.list_topics(chapter_id)

    async def get_tests(self, topic_id: int):
        return await self.tests_s.list_tests(topic_id)

    async def get_questions(self, test_id: int):
        return await self.quest_s.list_questions(test_id)

    async def get_answers(self, question_id: int):
        return await self.answer_s.list_answers(question_id)


async def main():
    dotenv.load_dotenv()
    db_path = os.getenv('PATH_DB')

    SUBJECTS_SERV = SubjectsService(SubjectsRepo(db_path))
    CHAPTERS_SERV = ChaptersService(ChaptersRepo(db_path))
    TOPICS_SERV = TopicsService(TopicsRepo(db_path))
    TESTS_SERV = TestsService(TestsRepo(db_path))
    QUESTIONS_SERV = QuestionsService(QuestionsRepo(db_path))
    ANSWERS_SERV = AnswersService(AnswersRepo(db_path))


    t = TestsDataService([SUBJECTS_SERV, CHAPTERS_SERV, TOPICS_SERV, TESTS_SERV, QUESTIONS_SERV, ANSWERS_SERV])
    await t.add_test('Математика', 'описание матем', 'Арифметика', 'Простые числа',
                     1, 'Вопрос Простые числа №1', '1.....2....3...4...5', 2)
    print('Предметы:',[i.name for i in await t.get_subjects()])
    print('Разделы:', [i.name for i in await t.get_chapters(1)])
    print('Темы:',[i.name for i in await t.get_topics(1)])
    print('Тесты:',[i.number for i in await t.get_tests(1)])
    print('Вопросы:',[i.text for i in await t.get_questions(1)])
    print('Ответ на вопрос:',[i.text for i in await t.get_answers(1)])


if __name__ == '__main__':
    asyncio.run(main())