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
                        `text` TEXT NOT NULL,
                        `subject_id` INTEGER,
                        `created_at` TEXT DEFAULT CURRENT_TIMESTAMP,

                        CONSTRAINT `topics_subjects` 
                        FOREIGN KEY (`subject_id`)
                        REFERENCES Subjects(`id`));
                        '''
        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript(sql_command)
            await db.commit()

    async def create_topic(self, sub_name: str, topic_text: str) -> None:

        sql_command = '''INSERT INTO `Topics`(`text`, `subject_id`)
                        VALUES (:topic_text, (SELECT `id` FROM `Subjects` WHERE `name` = :sub_name))'''
        async with (aiosqlite.connect(self.db_path) as db):
            db.row_factory = aiosqlite.Row
            data = ({"sub_name": sub_name,
                     "topic_text": topic_text})

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

    async def fetch_topics(self, sub_name: str) -> list[Topics] or None:

        sql_command = """
                        SELECT `id`, `text`, `subject_id`, `created_at` FROM `Topics`
                        WHERE `subject_id` = (SELECT `id` FROM `Subjects` WHERE `name` = ?);
                        """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(sql_command, [sub_name])
            all_topics = await cursor.fetchall()

            if all_topics is not None:
                all_topics = [Topics(*topic) for topic in all_topics]
            return all_topics

    async def remove_topic(self, topic_id: int) -> None:

        sql_command = """
                       DELETE FROM `Topics`
                       WHERE `id` = ? ;
                      """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql_command, [topic_id])
            await db.commit()
