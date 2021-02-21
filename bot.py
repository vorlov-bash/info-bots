import asyncio
import asyncpg
import sys

from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.config import load_config
from src.handlers.user import register_user
from src.middlewares.db import DbMiddleware, DbLogMiddleware
from src.middlewares.loguru import LoguruMiddleware


def setup_logger():
    # Delete default logger
    logger.remove()

    # Add custom loggers
    logger.add(sys.stderr, format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
               level='INFO')
    logger.add('logs/debug/debug_{time: YYYY-MM-DD}.log', format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
               level='DEBUG', encoding='utf-8')
    logger.add('logs/info/info_{time: YYYY-MM-DD}.log', format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
               level='INFO', encoding='utf-8')
    logger.add('logs/errors/errors_{time: YYYY-MM-DD}.log',
               format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
               level='ERROR', encoding='utf-8')


async def setup_psql(user, password, database, host) -> asyncpg.Pool:
    try:
        return await asyncpg.create_pool(user=user, password=password, database=database, host=host)
    except Exception as e:
        logger.error('Failed connect to postgres: ' + str(e))
        raise e


async def main():
    # pre-setup
    setup_logger()

    _conf_path = 'bot.yml'
    _config = load_config(_conf_path)
    logger.debug(f'✅ config loaded from {_conf_path}')
    async_pool = await setup_psql(
        user=_config.psql_db.user,
        password=_config.psql_db.password,
        database=_config.psql_db.database,
        host=_config.psql_db.host
    )

    logger.debug(f'✅ async postgres pool initialized')

    # setup
    bot = Bot(token=_config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_user(dp)
    logger.debug(f'✅ user handlers registered')

    dp.setup_middleware(DbMiddleware(async_pool, dp))
    dp.setup_middleware(DbLogMiddleware())
    dp.setup_middleware(LoguruMiddleware())
    logger.debug(f'✅ middleware setup successful')

    try:
        logger.debug('bot polling started...')
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
