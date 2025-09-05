from __future__ import annotations

import aiosqlite

from buisness_logic.db import Subjects


class SubjectsRepo:

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    async def init_table(self) -> None:

        sql_command = '''
                    CREATE TABLE IF NOT EXISTS `Subjects`(
                        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                        `name` TEXT NOT NULL,
                        `description` TEXT,
                        `created_at` TEXT DEFAULT CURRENT_TIMESTAMP);
                        '''
        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript(sql_command)
            await db.commit()

    async def create_subject(self, sub_name: str, description: str = None) -> None:

        sql_command = '''INSERT  INTO `Subjects`(`name`, `description`)
                        VALUES (:sub_name, :description)'''
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            data = ({"sub_name": sub_name,
                     "description": description})

            await db.execute(sql_command, data)
            await db.commit()

    #async def search_sub(self, sub_name: str) -> bool:
    #    sql_command = '''SELECT * FROM `Subjects` WHERE `name` = :sub_name'''
#
    #    data = ({"sub_name": sub_name})
#
    #    async with aiosqlite.connect(self.db_path) as db:
    #        db.row_factory = aiosqlite.Row
#
    #        cursor = await db.execute(sql_command, data)
    #        raw = await cursor.fetchone()
#
    #        if raw is not None:
    #            sub = Subjects(**dict(raw))
    #            if sub.name == sub_name:
    #                return True
    #        return False

    async def fetch_subjects(self) -> list[Subjects] | None:

        sql_command = """
                        SELECT * FROM `Subjects`;
                      """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(sql_command)
            all_subjects = await cursor.fetchall()

            if all_subjects is not None:
                all_subjects = [Subjects(*subject) for subject in all_subjects]
            return all_subjects

    async def remove_subject(self, sub_id: int) -> None:

        sql_command = """
                       DELETE FROM `Subjects`
                       WHERE `id` = ? ;
                      """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql_command, [sub_id])
            await db.commit()
