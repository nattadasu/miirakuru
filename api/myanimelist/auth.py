import json
import secrets
import webbrowser
from pathlib import Path
from typing import TypedDict, Union

from aiohttp import ClientSession

from .listener import get_code


class AuthData(TypedDict):
    """AuthData type hint."""
    token_type: str
    expires_in: int
    access_token: str
    refresh_token: str


class Auth:
    """Auth class for MyAnimeList."""
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        state: str = "RequestForToken",
        cache_file: Union[str, Path] = "./secrets/myanimelist.json",
    ) -> None:
        """
        Initializes the Auth class.

        Parameters
        ----------
        client_id: str
            The client id.
        client_secret: str
            The client secret.
        redirect_uri: str
            The redirect uri.
        state: str
            The state.
        cache_file: Union[str, Path]
            The cache file.

        Returns
        -------
        None
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        self.state = state
        self.code_challenge = self.get_new_code_verifier()
        self.auth_url = (
            "https://myanimelist.net/v1/oauth2/authorize"
            f"?response_type=code"
            f"&client_id={self.client_id}"
            f"&code_challenge={self.code_challenge}"
            f"&state={self.state}"
            f"&redirect_uri={self.redirect_uri}"
        )

        self.cache_file = Path(cache_file)
        self.is_authenticated = False
        self.auth_data: Union[None, AuthData] = None

    async def get_cache(self) -> bool:
        """
        Gets the cache file.

        Returns
        -------
        bool
            Whether the cache file exists or not.
        """
        if self.cache_file.exists():
            with open(self.cache_file) as file:
                self.auth_data = json.load(file)
            if not self.auth_data or not self.auth_data.get("token_type"):
                self.auth_data = None
                return False
        else:
            with open(self.cache_file, "w+") as file:
                json.dump({}, file)
            self.auth_data = None
            return False

        return True

    async def expired(self) -> bool:
        """
        Checks if the token is expired.

        Returns
        -------
        bool
            Whether the token is expired or not.
        """
        if not self.auth_data:
            return True

        url = "https://api.myanimelist.net/v2/users/@me"
        headers = {"Authorization": f"Bearer {self.auth_data['access_token']}"}

        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return response.status != 200

    async def authenticate(self) -> None:
        """
        Authenticates the user.

        Raises
        ------
        Exception
            If there is a problem getting the auth data, or the token.

        Returns
        -------
        None
        """
        await self.get_cache()
        if not await self.expired():
            return

        if not self.auth_data:
            webbrowser.open_new_tab(self.auth_url)

            code = await self.listen_for_auth_code()
            if not code:
                raise Exception("Problem listening for auth code.")

            data = await self.get_token(code)
            if not data:
                raise Exception("Problem getting auth data.")
            self.auth_data = data
        else:
            if not self.auth_data or not self.auth_data.get("token_type"):
                raise Exception("Problem getting auth data.")
            self.auth_data = await self.get_new_token()

        with open(self.cache_file, "w+") as file:
            json.dump(self.auth_data, file)

        self.is_authenticated = True

    async def get_token(self, code: str) -> dict:
        """
        Gets the token from the code.

        Parameters
        ----------
        code: str
            The code to get the token from.

        Returns
        -------
        dict
            The token.
        """
        base_url = "https://myanimelist.net/v1/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "code_verifier": self.code_challenge,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }

        async with ClientSession() as session:
            async with session.post(base_url, data=data, headers=headers) as response:
                response.raise_for_status()
                return await response.json()

    async def get_new_token(self) -> dict:
        """
        Gets a new token from the refresh token.

        Returns
        -------
        dict
            The new token.
        """
        if not self.auth_data:
            raise Exception("No Auth data or refresh_token")
        if not self.auth_data.get("refresh_token"):
            raise Exception("No Auth data")

        base_url = "https://myanimelist.net/v2/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "redirect_uri": self.redirect_uri,
            "refresh_token": self.auth_data["refresh_token"],
        }

        async with ClientSession() as session:
            async with session.post(base_url, data=data, headers=headers) as response:
                response.raise_for_status()
                return await response.json()

    @staticmethod
    async def listen_for_auth_code() -> str:
        """
        Listens for the auth code.

        Returns
        -------
        str
            The auth code.
        """
        code = await get_code()

        if not code:
            raise Exception("No output")

        return code

    @staticmethod
    def get_new_code_verifier() -> str:
        """
        Gets a new code verifier.

        Returns
        -------
        str
            The code verifier.
        """
        token = secrets.token_urlsafe(100)
        return token[:128]
