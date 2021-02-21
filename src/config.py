from yaml import load as _load
from yaml import Loader as _Loader

from dataclasses import dataclass
from loguru import logger


@dataclass
class TgBot:
    token: str
    admin_id: int


@dataclass
class PostgresDbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class Config:
    tg_bot: TgBot
    psql_db: PostgresDbConfig


def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes")


def load_config(path: str) -> Config:
    with open(path, 'r') as config_file:
        config = _load(config_file.read(), Loader=_Loader)
        tg_bot = config['tg_bot']
        return Config(
            tg_bot=TgBot(
                token=tg_bot['token'],
                admin_id=int(tg_bot['admin_id'])
            ),
            psql_db=PostgresDbConfig(**config['db'])
        )
