from __future__ import annotations

from sqlite3 import IntegrityError
from buisness_logic.repo.chapters_repo import ChaptersRepo
from buisness_logic.db import Chapters


class ChaptersService:

    def __init__(self, repo: ChaptersRepo):
        self.repo = repo

    def search_chapter_name(self, chapter_name: str, list_chapters: list[Chapters]) -> bool:
        for chapter in list_chapters:
            if chapter.name == chapter_name:
                return True
        return False

    async def add_chapter(self, sub_id: int, chapter_name: str) -> None:

        """
        :param sub_id: int,
        :param chapter_name: str
        :return: None
        """
        await self.repo.init_table()

        if self.search_chapter_name(chapter_name, await self.repo.fetch_chapters(sub_id)):
            return
        await self.repo.create_chapter(sub_id, chapter_name)

    async def list_chapters(self, sub_id: int) -> list[Chapters]:

        """
        :param sub_id: int
        :return: list[Chapters]
        """
        return await self.repo.fetch_chapters(sub_id)

    async def remove_chapter(self, sub_id: int, chapter_name: str) -> None:

        """
        :param sub_id: int,
        :param chapter_name: str,
        :return: None
        """
        if not self.search_chapter_name(chapter_name, await self.repo.fetch_chapters(sub_id)):
            raise IntegrityError
        await self.repo.remove_chapter(sub_id, chapter_name)

    async def find_id(self, sub_id: int, chapter_name: str) -> int | None:
        chapters = await self.list_chapters(sub_id)
        for chapter in chapters:
            if chapter.name == chapter_name:
                return chapter.id

