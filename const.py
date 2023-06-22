from dataclasses import asdict, dataclass
from typing import Literal

from yaml import safe_load

with open("secrets.yaml", "r") as f:
    secrets: dict[str, dict[str, str | int | None]] = safe_load(f)


@dataclass
class Discord:
    """Discord bot configuration"""

    token = str(secrets["bot_config"]["token"])
    """Discord bot token"""
    client_id = str(secrets["bot_config"]["client_id"])
    """Discord bot client ID"""
    server_id = str(secrets["bot_config"]["server_id"])
    """Discord server ID"""
    channel_id = str(secrets["bot_config"]["channel_id"])
    """Channel ID to send activity messages to"""


@dataclass
class OauthBase:
    """Oauth client base"""

    client_id: str | int
    """Client ID"""
    client_secret: str | int | None
    """Client secret, for MyAnimeList, must be none if app_type != web"""
    redirect_uri: str
    """Redirect URI, must starts at http://localhost:5000/"""


@dataclass
class MyAnimeListOauth(OauthBase):
    """MyAnimeList OAuth Information"""

    app_type: Literal["web", "ios", "android", "other"]
    """App type listed in MyAnimeList API info"""


@dataclass
class AniListOauth(OauthBase):
    """AniList OAuth Information"""


@dataclass
class SimklOauth(OauthBase):
    """SIMKL OAuth Information"""


@dataclass
class TraktOauth(OauthBase):
    """Trakt OAuth Information"""


@dataclass
class KitsuOauth:
    """Kitsu configuration"""

    client_id = secrets["kitsu"]["client_id"]
    """Kitsu client ID"""
    client_secret = secrets["kitsu"]["client_secret"]
    """Kitsu client secret"""
    email = secrets["kitsu"]["email"]
    """Kitsu email"""
    password = secrets["kitsu"]["password"]
    """Kitsu password"""


@dataclass
class Constants:
    """Constants"""

    discord = Discord()
    """Discord bot configuration"""
    myanimelist = MyAnimeListOauth(**secrets["myanimelist"])  # type: ignore
    """MyAnimeList configuration"""
    anilist = AniListOauth(**secrets["anilist"])  # type: ignore
    """AniList configuration"""
    simkl = SimklOauth(**secrets["simkl"])  # type: ignore
    """SIMKL configuration"""
    trakt = TraktOauth(**secrets["trakt"])  # type: ignore
    """Trakt configuration"""
    kitsu = KitsuOauth
    """Kitsu configuration"""

    def to_dict(self):
        """Convert dataclass to a dict"""
        return asdict(self)


const = Constants()

__all__ = [
    "const",
    "Constants",
    "Discord",
    "MyAnimeListOauth",
    "SimklOauth",
    "TraktOauth",
    "KitsuOauth"
]
