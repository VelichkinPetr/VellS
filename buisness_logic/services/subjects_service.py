from __future__ import annotations
import asyncio

from sqlite3 import IntegrityError
from buisness_logic.repo.subjects_repo import SubjectsRepo
from buisness_logic.db import Subjects


class SubjectsService:

    def __init__(self, repo: SubjectsRepo):
        self.repo = repo

    def search_sub_name(self, sub_name: str, list_sub: list[Subjects]) -> bool:
        for sub in list_sub:
            if sub.name == sub_name:
                return True
        return False

    def search_sub_id(self, sub_id: int, list_sub: list[Subjects]) -> bool:
        for sub in list_sub:
            if sub.id == sub_id:
                return True
        return False

    async def add_subject(self, sub_name: str, description: str) -> None:

        """
        :param sub_name: str,
        :param description: str
        :return: None
        """

        await self.repo.init_table()

        if self.search_sub_name(sub_name, await self.repo.fetch_subjects()):
            return
        await self.repo.create_subject(sub_name, description)

    async def list_subjects(self) -> list[Subjects]:

        """
        :return: list
        """
        return await self.repo.fetch_subjects()

    async def remove_subjects(self, sub_id: int) -> None:

        """
        :param sub_id: int,
        :return: None
        """

        if not self.search_sub_id(sub_id, await self.repo.fetch_subjects()):
            raise IntegrityError
        await self.repo.remove_subject(sub_id)

    async def find_id(self, sub_name: str) -> int | None:
        subjects = await self.list_subjects()
        for subject in subjects:
            if subject.name == sub_name:
                return subject.id
