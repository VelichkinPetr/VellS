from __future__ import annotations

import aiosqlite

from buisness_logic.db import Answers


class AnswersRepo:

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    async def init_table(self) -> None:

        sql_command = '''
                    CREATE TABLE IF NOT EXISTS `Answers`(
                        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                        `question_id` INTEGER,
                        `text` TEXT NOT NULL,
                        `created_at` TEXT DEFAULT CURRENT_TIMESTAMP,
                        `is_correct` INTEGER UNSIGNED,

                        CONSTRAINT `answers_questions` 
                        FOREIGN KEY (`question_id`)
                        REFERENCES Questions(`id`));
                        '''
        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript(sql_command)
            await db.commit()

    async def create_answer(self, quest_id: int, answers: str, is_correct: int):

        sql_command = '''INSERT INTO `Answers`(`text`, `question_id`, `is_correct`)
                        VALUES (:answers, :quest_id, :is_correct)'''
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            data = ({"answers": answers,
                     "quest_id": quest_id,
                     "is_correct": is_correct})

            await db.execute(sql_command, data)
            await db.commit()

    async def fetch_answers(self, question_id: int) -> list[Answers] | None:

        sql_command = """
                        SELECT * FROM `Answers`
                        WHERE `question_id` = ?;
                      """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(sql_command, [question_id])
            all_answers = await cursor.fetchall()

            if all_answers is not None:
                all_answers = [Answers(*answer) for answer in all_answers]
            return all_answers

    async def remove_answer(self, question_id: int, answer_id: int) -> None:

        sql_command = """
                       DELETE FROM `Answers`
                       WHERE `question_id` = ? AND `id` = ?;
                      """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql_command, [question_id, answer_id])
            await db.commit()
