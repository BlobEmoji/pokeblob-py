import logging

from discord.ext.commands import Bot


class PokeBlob(Bot):
    def __init__(self, *args, db, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = db
        self.logger = logging.getLogger(__name__)

    async def on_ready(self):
        self.logger.info('Ready! Logged in as %s (%d)', self.user, self.user.id)
