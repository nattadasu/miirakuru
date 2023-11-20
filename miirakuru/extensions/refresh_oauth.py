from json import load

from interactions import (AutoShardedClient, Client, Extension,
                          IntervalTrigger, Task)

from const import Constants
from models.secrets import OauthToken


class RefreshOAuth(Extension):
    """Automatically refreshes OAuth token for the user when it expires."""

    def __init__(self, bot: Client | AutoShardedClient):
        self.bot = bot

        self.refresh_oauth.start()

    @Task.create(trigger=IntervalTrigger(minutes=5))
    async def refresh_oauth(self):
        """Refresh OAuth token for the user when it expires."""
        config = Constants()

        paths = [
            'myanimelist'
        ]

        for path in paths:
            path = f"secrets/{path}.json"
            oauth_token = self._path_to_oauth_token(path)

    @staticmethod
    def _path_to_oauth_token(path: str) -> OauthToken:
        """Get OAuth token from path"""
        with open(path, 'r') as f:
            return OauthToken(**load(f))
