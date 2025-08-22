from __future__ import annotations


import aiosqlite

from buisness_logic.db import Tests


class TestsRepo:

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    async def init_table(self) -> None:

        sql_command = ''' 
                    CREATE TABLE IF NOT EXISTS `Tests`(
                        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                        `number` INTEGER UNSIGNED,
                        `topic_id` INTEGER,
                        `created_at` TEXT DEFAULT CURRENT_TIMESTAMP,
                        
                        CONSTRAINT `tests_topics` 
                        FOREIGN KEY (`topic_id`)
                        REFERENCES Topics(`id`));
                    '''
        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript(sql_command)
            await db.commit()

    async def create_test(self, topic_id: int, test_num: int) -> None:
        # (SELECT `id` FROM `Topics` WHERE `text` = :topic_text))
        sql_command = '''INSERT INTO `Tests`(`number`, `topic_id`)   
                        VALUES (:test_num, :topic_id) '''
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            data = ({"test_num": test_num,
                     "topic_id": topic_id})

            await db.execute(sql_command, data)
            await db.commit()

    async def fetch_tests(self, topic_id: int) -> list[Tests] | None:

        sql_command = """
                        SELECT * FROM `Tests`
                        WHERE `topic_id` = ? ;
                        """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(sql_command, [topic_id])
            all_tests = await cursor.fetchall()

            if all_tests is not None:
                all_tests = [Tests(*test) for test in all_tests]
            return all_tests

    async def remove_test(self, topic_id: int, test_num: int) -> None:

        sql_command = """
                       DELETE FROM `Tests`
                       WHERE `topic_id` = ? AND `number` = ?;
                      """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql_command, [topic_id, test_num])
            await db.commit()
