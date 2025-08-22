from __future__ import annotations

import aiosqlite

from buisness_logic.db import Topics


class TopicsRepo:

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    async def init_table(self) -> None:

        sql_command = '''
                    CREATE TABLE IF NOT EXISTS `Topics`(
                        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                        `name` TEXT NOT NULL,
                        `chapter_id` INTEGER,
                        `created_at` TEXT DEFAULT CURRENT_TIMESTAMP,

                        CONSTRAINT `topics_chapters` 
                        FOREIGN KEY (`chapter_id`)
                        REFERENCES Chapters(`id`));
                        '''
        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript(sql_command)
            await db.commit()

    async def create_topic(self, chapter_id: int, topic_name: str) -> None:

        sql_command = '''INSERT INTO `Topics`(`name`, `chapter_id`)
                        VALUES (:topic_name, :chapter_id)'''
        async with (aiosqlite.connect(self.db_path) as db):
            db.row_factory = aiosqlite.Row
            data = ({"chapter_id": chapter_id,
                     "topic_name": topic_name})

            await db.execute(sql_command, data)
            await db.commit()

    #async def search_topic(self, topic_text: str):
    #    sql_command = '''SELECT * FROM `Topics` WHERE `text` = :topic_text'''
#
    #    data = ({"topic_text": topic_text})
#
    #    async with aiosqlite.connect(self.db_path) as db:
    #        db.row_factory = aiosqlite.Row
#
    #        cursor = await db.execute(sql_command, data)
    #        raw = await cursor.fetchone()
#
    #        if raw is not None:
    #            topic = Topics(**dict(raw))
    #            if topic.text == topic_text:
    #                return True
    #        return False

    async def fetch_topics(self, chapter_id: int) -> list[Topics] | None:

        sql_command = """
                        SELECT `id`, `name`, `chapter_id`, `created_at` FROM `Topics`
                        WHERE `chapter_id` = ?;
                        """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(sql_command, [chapter_id])
            all_topics = await cursor.fetchall()

            if all_topics is not None:
                all_topics = [Topics(*topic) for topic in all_topics]
            return all_topics

    async def remove_topic(self, chapter_id: int, topic_name: str) -> None:

        sql_command = """
                       DELETE FROM `Topics`
                       WHERE `name` = ?  AND `chapter_id` = ?;
                      """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql_command, [topic_name, chapter_id])
            await db.commit()
