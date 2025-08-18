from __future__ import annotations

import asyncio
import os

import aiosqlite
import dotenv

from buisness_logic.db import Subjects, Tests, Topics, Questions, Answers

class TestsRepo:

    def __init__(self, db_path: str) -> None:
        dotenv.load_dotenv()
        self.db_path = os.getenv('PATH_DB')

    async def init_tables(self) -> None:

        sql_command = '''
                    CREATE TABLE IF NOT EXISTS `Subjects`(
                        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                        `name` TEXT NOT NULL UNIQUE,
                        `description` TEXT,
                        `created_at` TEXT DEFAULT CURRENT_TIMESTAMP);
                        
                    CREATE TABLE IF NOT EXISTS `Topics`(
                        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                        `text` TEXT NOT NULL,
                        `subject_id` INTEGER,
                        `created_at` TEXT DEFAULT CURRENT_TIMESTAMP,
                        
                        CONSTRAINT `topics_subjects` 
                        FOREIGN KEY (`subject_id`)
                        REFERENCES Subjects(`id`));
                    
                    CREATE TABLE IF NOT EXISTS `Tests`(
                        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                        `topic_id` INTEGER,
                        `created_at` TEXT DEFAULT CURRENT_TIMESTAMP,
                        
                        CONSTRAINT `tests_topics` 
                        FOREIGN KEY (`topic_id`)
                        REFERENCES Topics(`id`));
                        
                    CREATE TABLE IF NOT EXISTS `Questions`(
                        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                        `test_id` INTEGER,
                        `text` TEXT NOT NULL,
                        `created_at` TEXT DEFAULT CURRENT_TIMESTAMP,
                        
                        CONSTRAINT `questions_topics` 
                        FOREIGN KEY (`test_id`)
                        REFERENCES Tests(`id`));
                        
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

    async def create_test(self, sub_name: str, description: str,
                          topic_text: str, quest_text: str,
                          answers: str, is_correct: int):

        sql_commands = ['''INSERT  INTO `Subjects`(`name`, `description`)
                        VALUES (:sub_name, :description)''',

                        '''INSERT INTO `Topics`(`text`, `subject_id`)
                        VALUES (:topic_text, (SELECT `id` FROM `Subjects` WHERE `name` = :sub_name))''',

                        '''INSERT INTO `Tests`(`topic_id`)
                        VALUES ((SELECT `id` FROM `Topics` WHERE `text` = :topic_text))''',

                        '''INSERT INTO `Questions`(`text`, `test_id`)
                        VALUES (:quest_text, 
                                (SELECT `Tests`.`id` FROM `Tests` 
                                INNER JOIN `Topics` ON `topic_id` = `Topics`.`id` 
                                WHERE `Topics`.`text` = :topic_text))''',

                        '''INSERT INTO `Answers`(`text`, `question_id`, `is_correct`)
                        VALUES (:answers, 
                                (SELECT `id` FROM `Questions` WHERE `text` = :quest_text), :is_correct)''',]

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            data = (
                {"sub_name": sub_name, "description": description},
                {"topic_text": topic_text, "sub_name": sub_name},
                {"topic_text": topic_text},
                {"quest_text": quest_text, "topic_text": topic_text},
                {"answers": answers, "quest_text": quest_text, "is_correct": is_correct},
            )

            for i, sql_command in enumerate(sql_commands):
                await db.execute(sql_command, data[i])

            await db.commit()
    async def get_data(self, sub_name: str, topic_text: str,
                       quest_text: str, answers: str):

        sql_commands = [
            '''SELECT * FROM `Subjects` WHERE `name` = :sub_name''',

            '''SELECT * FROM `Topics` WHERE `text` = :topic_text''',

            '''SELECT * FROM `Tests` 
            WHERE `topic_id` = (SELECT `id` FROM `Topics` WHERE `text` = :topic_text)''',

            '''SELECT * FROM `Questions` WHERE `text` = :quest_text''',

            '''SELECT * FROM `Answers` WHERE `text` = :answers''',
        ]

        data = (
            {"sub_name": sub_name},
            {"topic_text": topic_text},
            {"topic_text": topic_text},
            {"quest_text": quest_text},
            {"answers": answers}
        )
        objects = [Subjects, Topics, Tests, Questions, Answers]

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            for i, sql_command in enumerate(sql_commands):
                cursor = await db.execute(sql_command, data[i])
                raw = await cursor.fetchone()
                objects[i] = objects[i](**dict(raw))
        return objects


async def main():
    u = TestsRepo('path')
    await u.init_tables()
    test = await u.create_test('Биология','1','Организм','Ответь 1-4','1,2,3,4',1)
    #test_arg = await u.get_data('Биология','Организм человека', 'Ответь 1-4', '1,2,3,4')
    #[print(elem) for elem in test_arg]


if __name__ == '__main__':
    asyncio.run(main())

