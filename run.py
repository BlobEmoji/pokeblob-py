# -*- coding: utf-8 -*-

import asyncio
import logging
import sys

from pokeblob.bot import PokeBlob

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


# set default levels
logging.getLogger().setLevel(logging.INFO)
logging.getLogger('pokeblob').setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

# log file and stdout
handler = logging.FileHandler(filename='pokeblob.log', encoding='utf-8', mode='a')
handler.setFormatter(formatter)
stream = logging.StreamHandler(stream=sys.stdout)
stream.setFormatter(formatter)

logging.getLogger().addHandler(handler)
logging.getLogger().addHandler(stream)


bot = PokeBlob()
bot.run()
