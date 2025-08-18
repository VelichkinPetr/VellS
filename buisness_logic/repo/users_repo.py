from __future__ import annotations

import asyncio
import os

import aiosqlite
import dotenv

from buisness_logic.db import Users

class UsersRepo:

    def __init__(self, db_path: str) -> None:
        dotenv.load_dotenv()
        self.db_path = os.getenv('PATH_DB')

    async def init_table(self) -> None:

        sql_command = '''
                        CREATE TABLE IF NOT EXISTS `Users`(
                            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                            `telegram_id` INTEGER NOT NULL UNIQUE,
                            `user_name` TEXT NOT NULL,
                            `name` TEXT NOT NULL,
                            `surname` TEXT NOT NULL,
                            `role` INTEGER DEFAULT 0,
                            `registered_at` TEXT DEFAULT CURRENT_TIMESTAMP
                        );
                        '''

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql_command)
            await db.commit()

    async def create_user(self, telegram_id: int, user_name: str, name: str, surname: str):

        sql_command = '''
                        INSERT INTO `Users`(`telegram_id`, `user_name`, `name`, `surname`)
                        VALUES (?, ?, ?, ?);
                        '''
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            await db.execute(sql_command, [telegram_id, user_name, name, surname])
            await db.commit()

            cursor = await db.execute(
                '''SELECT * FROM `Users` WHERE `telegram_id` = ?''', [telegram_id]
            )

            raw_user = await cursor.fetchone()

            return Users(**dict(raw_user))


async def main():
    u = UsersRepo('path')
    await u.init_table()
    user = await u.create_user(2222, 'TaJIucMaH','Petr', 'Vel')
    print(user)

if __name__ == '__main__':
    asyncio.run(main())

