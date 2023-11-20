import time
from dataclasses import asdict, dataclass
from typing import Literal


@dataclass
class BaseOauthToken:
    """Base class for OauthToken and OauthTokenResponse"""
    access_token: str
    """Access token"""
    token_type: str
    """Token type"""
    expires_in: int
    """Expires in"""
    refresh_token: str
    """Refresh token"""
    scope: str | None = None
    """Scope"""
    created_at: int | None = None
    """Created at"""
    code_verifier: str | None = None
    """PKCE code verifier"""
    code_verifier_method: Literal["plain"] | None = None
    """PKCE code verifier method for checking code_challange"""

    def __post_init__(self):
        """Set created_at to current time if it is None"""
        self.created_at = int(
            time.time()) if self.created_at is None else self.created_at

    def is_expired(self):
        """Check if token is expired"""
        if self.created_at and self.expires_in:
            return self.created_at + self.expires_in < int(time.time())
        raise ValueError(
            "It seems `created_at` or `expires_in` does not have type of int as a value")

    def to_dict(self):
        """Convert to dict"""
        return asdict(self)


@dataclass
class OauthToken(BaseOauthToken):
    """Oauth token"""


__all__ = ['OauthToken']
