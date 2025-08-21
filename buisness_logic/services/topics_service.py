from __future__ import annotations
import asyncio

from sqlite3 import IntegrityError
from buisness_logic.repo.topics_repo import TopicsRepo
from buisness_logic.db import Topics


class TopicsService:

    def __init__(self, repo: TopicsRepo):
        self.repo = repo

    def search_topic_text(self, topic_text: str, list_topics: list[Topics]) -> bool:
        for topic in list_topics:
            if topic.text == topic_text:
                return True
        return False

    def search_topic_id(self, topic_id: int, list_topics: list[Topics]) -> bool:
        for topic in list_topics:
            if topic.id == topic_id:
                return True
        return False

    async def add_topic(self, sub_name: str, topic_text: str) -> None:

        """
        :param sub_name: str,
        :param topic_text: str
        :return: None
        """
        await self.repo.init_table()

        if self.search_topic_text(topic_text, await self.repo.fetch_topics(sub_name)):
            return
        await self.repo.create_topic(sub_name, topic_text)

    async def list_topics(self, sub_name: str) -> list[Topics]:

        """
        :param sub_name: str
        :return: list[Topics]
        """
        return await self.repo.fetch_topics(sub_name)

    async def remove_topic(self, sub_name: str, topic_id: int) -> None:

        """
        :param sub_name: str,
        :param topic_id: int,
        :return: None
        """
        if not self.search_topic_id(topic_id, await self.repo.fetch_topics(sub_name)):
            raise IntegrityError
        await self.repo.remove_topic(topic_id)

    async def find_id(self, sub_name: str, topic_text: str):
        topics = await self.list_topics(sub_name)
        for topic in topics:
            if topic.text == topic_text:
                return topic.id

