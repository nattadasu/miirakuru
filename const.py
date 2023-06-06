from dataclasses import dataclass, asdict
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
class Features:
    """Features"""

    anilist: bool = secrets["features"]["anilist"]
    """Enable AniList sync"""
    annict: bool = secrets["features"]["annict"]
    """Enable Annict sync"""
    kitsu: bool = secrets["features"]["kitsu"]
    """Enable Kitsu sync"""
    trakt: bool = secrets["features"]["trakt"]
    """Enable Trakt sync"""
    simkl: bool = secrets["features"]["simkl"]
    """Enable SIMKL sync"""


@dataclass
class CommonTaskTimeDelta:
    """Common task time delta configuration"""

    minutes: int = 0
    """Minutes"""
    hours:   int = 0
    """Hours"""
    days:    int = 0
    """Days"""


@dataclass
class Tasks:
    """Tasks configuration"""

    update_oauth_keys = CommonTaskTimeDelta(
        **secrets["tasks"]["update_oauth_keys"])
    """Check time interval for updating OAuth keys"""
    update_user_activity = CommonTaskTimeDelta(
        **secrets["tasks"]["update_user_activity"])


@dataclass
class OauthBase:
    """Oauth client base"""

    client_id: str | int
    """Client ID"""
    client_secret: str | int
    """Client secret"""
    redirect_uri: str
    """Redirect URI, must starts at http://localhost:5000/"""


@dataclass
class MyAnimeListOauth(OauthBase):
    """MyAnimeList OAuth Information"""

    client_secret: str | int | None
    """Client secret, must be none if app_type != web"""
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


MyAnimeListOauth = MyAnimeListOauth(**secrets["myanimelist"])
AniListOauth = AniListOauth(**secrets["anilist"])
SimklOauth = SimklOauth(**secrets["simkl"])
TraktOauth = TraktOauth(**secrets["trakt"])


@dataclass
class KitsuOauth:
    """Kitsu configuration"""

    client_id     = secrets["kitsu"]["client_id"]
    """Kitsu client ID"""
    client_secret = secrets["kitsu"]["client_secret"]
    """Kitsu client secret"""
    email         = secrets["kitsu"]["email"]
    """Kitsu email"""
    password      = secrets["kitsu"]["password"]
    """Kitsu password"""


@dataclass
class Constants:
    """Constants"""

    discord     = Discord()
    """Discord bot configuration"""
    features    = Features()
    """Manage sync setting"""
    tasks       = Tasks()
    """Tasks configuration"""
    myanimelist = MyAnimeListOauth
    """MyAnimeList configuration"""
    anilist     = AniListOauth
    """AniList configuration"""
    simkl       = SimklOauth
    """SIMKL configuration"""
    trakt       = TraktOauth
    """Trakt configuration"""
    kitsu       = KitsuOauth
    """Kitsu configuration"""

    def to_dict(self):
        """Convert dataclass to a dict"""
        return asdict(self)


const = Constants()

__all__ = [
    "const",
    "Constants",
    "Discord",
    "Tasks",
    "MyAnimeListOauth",
    "SimklOauth",
    "TraktOauth",
    "KitsuOauth"
]
