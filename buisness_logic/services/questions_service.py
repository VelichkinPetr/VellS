from __future__ import annotations
import asyncio

from sqlite3 import IntegrityError
from buisness_logic.repo.questions_repo import QuestionsRepo
from buisness_logic.db import Questions


class QuestionsService:

    def __init__(self, repo: QuestionsRepo):
        self.repo = repo

    def search_question_id(self, quest_id: int, list_questions: list[Questions]) -> bool:
        for question in list_questions:
            if question.id == quest_id:
                return True
        return False

    async def add_question(self, test_id: int, quest_text: str) -> None:

        """
        :param test_id: int,
        :param quest_text: str
        :return: None
        """
        await self.repo.init_table()

        await self.repo.create_question(test_id, quest_text)

    async def list_questions(self, test_id: int) -> list[Questions]:

        """
        :param test_id: int
        :return: list[Questions]
        """
        return await self.repo.fetch_questions(test_id)

    async def remove_question(self, test_id: int, quest_id: int) -> None:

        """
        :param test_id: int,
        :param quest_id: int,
        :return: None
        """
        if not self.search_question_id(quest_id, await self.repo.fetch_questions(test_id)):
            raise IntegrityError
        await self.repo.remove_question(test_id, quest_id)

    async def find_id(self, test_id: int, quest_text: str):
        questions = await self.list_questions(test_id)
        for question in questions:
            if question.text == quest_text:
                return question.id
