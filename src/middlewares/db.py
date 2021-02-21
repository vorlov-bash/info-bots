import asyncpg
import aiogram
from aiogram import types

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware, BaseMiddleware

from src.services.repository import Repo


class DbMiddleware(LifetimeControllerMiddleware):
    def __init__(self, pool: asyncpg.Pool, dp: aiogram.Dispatcher):
        super().__init__()
        self.pool = pool
        self.dp = dp

    async def pre_process(self, obj, data, *args):
        db = await self.pool.acquire()
        data["db"] = db
        data["repo"] = Repo(db)

    async def post_process(self, obj, data, *args):
        del data["repo"]
        db = data.get("db")
        if db:
            await db.close()


class DbLogMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def on_pre_process_update(self, update: types.Update, data: dict):
        await data['repo'].log_update(update.message.from_user.id, update.as_json())
