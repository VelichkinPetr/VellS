from __future__ import annotations
import asyncio

from sqlite3 import IntegrityError
from buisness_logic.repo.topics_repo import TopicsRepo
from buisness_logic.db import Topics


class TopicsService:

    def __init__(self, repo: TopicsRepo):
        self.repo = repo

    def search_topic_name(self, topic_name: str, list_topics: list[Topics]) -> bool:
        for topic in list_topics:
            if topic.name == topic_name:
                return True
        return False

    async def add_topic(self, chapter_id: int, topic_name: str) -> None:

        """
        :param chapter_id: int,
        :param topic_name: str
        :return: None
        """
        await self.repo.init_table()

        if self.search_topic_name(topic_name, await self.repo.fetch_topics(chapter_id)):
            return
        await self.repo.create_topic(chapter_id, topic_name)

    async def list_topics(self, chapter_id: int) -> list[Topics]:

        """
        :param chapter_id: int
        :return: list[Topics]
        """
        return await self.repo.fetch_topics(chapter_id)

    async def remove_topic(self, chapter_id: int, topic_name: str) -> None:

        """
        :param chapter_id: int,
        :param topic_name: str,
        :return: None
        """
        if not self.search_topic_name(topic_name, await self.repo.fetch_topics(chapter_id)):
            raise IntegrityError
        await self.repo.remove_topic(chapter_id, topic_name)

    async def find_id(self, chapter_id: int, topic_name: str):
        topics = await self.list_topics(chapter_id)
        for topic in topics:
            if topic.name == topic_name:
                return topic.id

