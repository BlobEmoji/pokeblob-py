# -*- coding: utf-8 -*-

import asyncio
import asyncpg
import logging
import uvloop
import sys

import config
from pokeblob.bot import PokeBlob

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# set default levels
logging.getLogger().setLevel(logging.INFO)
logging.getLogger('pokeblob').setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

# log file and stdout
handler = logging.FileHandler(filename='pokeblobs.log', encoding='utf-8', mode='a')
handler.setFormatter(formatter)
stream = logging.StreamHandler(stream=sys.stdout)
stream.setFormatter(formatter)

logging.getLogger().addHandler(handler)
logging.getLogger().addHandler(stream)

async def main():
    logger = logging.getLogger('run')

    while True:
        try:
            db = await asyncpg.create_pool(**config.pg_credentials)
        except (ConnectionRefusedError, asyncpg.CannotConnectNowError):
            logger.exception('Cannot connect to Postgres, stalling:')
            await asyncio.sleep(2)
        else:
            break

    bot = PokeBlob(db=db, command_prefix='p!')
    logger.info('Running bot.')
    await bot.start(config.token)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
