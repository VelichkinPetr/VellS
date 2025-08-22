from __future__ import annotations

import aiosqlite

from buisness_logic.db import Questions


class QuestionsRepo:

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    async def init_table(self) -> None:

        sql_command = '''
                    CREATE TABLE IF NOT EXISTS `Questions`(
                        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                        `test_id` INTEGER,
                        `text` TEXT NOT NULL,
                        `created_at` TEXT DEFAULT CURRENT_TIMESTAMP,

                        CONSTRAINT `questions_topics` 
                        FOREIGN KEY (`test_id`)
                        REFERENCES Tests(`id`));
                        '''

        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript(sql_command)
            await db.commit()

    async def create_question(self, test_id: int, quest_text: str) -> None:

        sql_command = '''INSERT INTO `Questions`(`text`, `test_id`)
                        VALUES (:quest_text, :test_id)'''
        async with (aiosqlite.connect(self.db_path) as db):
            db.row_factory = aiosqlite.Row
            data = ({"quest_text": quest_text,
                     "test_id": test_id})

            await db.execute(sql_command, data)
            await db.commit()

    async def fetch_questions(self, test_id: int) -> list[Questions] | None:

        sql_command = """
                        SELECT * FROM `Questions`
                        WHERE `test_id` = ?;
                      """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(sql_command, [test_id])
            all_questions = await cursor.fetchall()

            if all_questions is not None:
                all_questions = [Questions(*question) for question in all_questions]
            return all_questions

    async def remove_question(self, test_id: int, quest_id: int) -> None:

        sql_command = """
                       DELETE FROM `Questions`
                       WHERE `test_id` = ? AND `id` = ?;
                      """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql_command, [test_id, quest_id])
            await db.commit()
