from __future__ import annotations
import asyncio

from sqlite3 import IntegrityError
from buisness_logic.repo.test_repo import TestsRepo
from buisness_logic.db import Tests


class TestsService:

    def __init__(self, repo: TestsRepo):
        self.repo = repo

    def search_test_num(self, test_num: int, list_tests: list[Tests]) -> bool:
        for test in list_tests:
            if test.number == test_num:
                return True
        return False

    async def add_test(self, topic_id: int, test_num: int) -> None:

        """
        :param topic_id: int,
        :param test_num: int
        :return: None
        """
        await self.repo.init_table()

        if self.search_test_num(test_num, await self.repo.fetch_tests(topic_id)):
            return
        await self.repo.create_test(topic_id, test_num)

    async def list_tests(self, topic_id: int) -> list[Tests]:

        """
        :param topic_id: int
        :return: list[Tests]
        """
        return await self.repo.fetch_tests(topic_id)

    async def remove_test(self, topic_id: int, test_num: int) -> None:

        """
        :param topic_id: int,
        :param test_num: int,
        :return: None
        """
        if not self.search_test_num(test_num, await self.repo.fetch_tests(topic_id)):
            raise IntegrityError
        await self.repo.remove_test(topic_id, test_num)

    async def find_id(self, topic_id: int, test_num: int):
        tests = await self.list_tests(topic_id)
        for test in tests:
            if test.number == test_num:
                return test.id
