from typing import List
from asyncpg import Connection

import json


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn: Connection = conn

    # users
    async def add_user(self, user_id) -> None:
        """Store user in DB, ignore duplicates"""
        await self.conn.execute(
            "INSERT INTO pythonbot.tg_users(user_id) VALUES ($1) ON CONFLICT DO NOTHING",
            user_id,
        )
        return

    async def log_update(self, user_id, update) -> None:
        await self.conn.execute(
            'insert into pythonbot.update_log(user_id, update) values ($1, $2) on conflict do nothing',
            user_id, update
        )
    # async def list_users(self) -> List[int]:
    #     """List all bot users"""
    #     return [
    #         row[0]
    #         async for row in self.conn.execute(
    #             "select userid from tg_users",
    #         )
    #     ]
