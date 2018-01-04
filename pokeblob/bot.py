# -*- coding: utf-8 -*-

import asyncio
import logging

import asyncpg
import yaml
from discord.ext import commands


class PokeBlob(commands.Bot):
    def __init__(self, *args, **kwargs):
        with open('config.yaml', 'rb') as f:
            self.config = config = yaml.safe_load(f)

        super().__init__(command_prefix=config['prefix'], *args, **kwargs)

        self.db = None
        self.logger = logging.getLogger(__name__)

        self.load_extension('jishaku')

    async def on_ready(self):
        self.logger.info('Ready! Logged in as %s (%d)', self.user, self.user.id)

    async def is_owner(self, user):
        return user.id in self.config['admin_users']

    async def start(self, *args, **kwargs):
        while True:
            # to allow Docker to set up PostgreSQL attempt to reconnect every 2 seconds
            try:
                self.db = await asyncpg.create_pool(**self.config['pg_credentials'])
            except (asyncpg.CannotConnectNowError, ConnectionRefusedError):
                self.logger.exception('Cannot connect to PostgreSQL, stalling:')
                await asyncio.sleep(2)
            else:
                break

        await super().start(*args, **kwargs)

    def run(self, *args, **kwargs):
        super().run(self.config['token'], *args, **kwargs)
