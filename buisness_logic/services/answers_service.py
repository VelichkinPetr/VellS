from __future__ import annotations
import asyncio

from sqlite3 import IntegrityError
from buisness_logic.repo.answers_repo import AnswersRepo
from buisness_logic.db import Answers


class AnswersService:

    def __init__(self, repo: AnswersRepo):
        self.repo = repo

    def search_answer_id(self, answer_id: int, list_answers: list[Answers]) -> bool:
        for answer in list_answers:
            if answer.id == answer_id:
                return True
        return False

    async def add_answer(self, quest_id: int, answers: str, is_correct: int) -> None:

        """
        :param quest_id: int,
        :param answers: str,
        :param is_correct: int
        :return: None
        """
        await self.repo.init_table()

        await self.repo.create_answer(quest_id, answers, is_correct)

    async def list_answers(self, question_id: int) -> list[Answers]:

        """
        :param question_id:
        :return: list[Answers]
        """
        return await self.repo.fetch_answers(question_id)

    async def remove_answer(self, question_id: int, answer_id: int) -> None:

        """
        :param question_id: int,
        :param answer_id: int,
        :return: None
        """
        if not self.search_answer_id(answer_id, await self.repo.fetch_answers(question_id)):
            raise IntegrityError
        await self.repo.remove_answer(question_id, answer_id)
