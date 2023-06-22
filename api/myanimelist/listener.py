import ctypes
import logging
import click
import typing as t

from multiprocessing import Process, Manager, Value
from flask import Flask, request
import asyncio


def flask_keep_quiet():
    """
    Prevents Flask from printing to stdout.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    def echo(
        message: t.Optional[t.Any] = None,
        file: t.Optional[t.IO] = None,
        nl: bool = True,
        err: bool = False,
        color: t.Optional[bool] = None,
        **styles: t.Any,
    ) -> None:
        """
        A dummy function to replace click.echo and click.secho.

        Parameters
        ----------
        message: Optional[Any]
            The message to print.
        file: Optional[IO]
            The file to print to.
        nl: bool
            Whether to print a newline or not.
        err: bool
            Whether to print to stderr or not.
        color: Optional[bool]
            Whether to print in color or not.
        **styles: Any
            The styles to print with.

        Returns
        -------
        None
        """

    click.echo = echo
    click.secho = echo


async def get_code(port: int = 8000) -> str:
    """
    Gets the code from the redirect uri.

    Parameters
    ----------
    port: int
        The port to run the server on.

    Returns
    -------
    str
        The code.
    """
    flask_keep_quiet()

    app = Flask("ServiceShouldStop")
    server = Process(target=lambda: app.run(port=port))
    manager = Manager()

    code = manager.Value(ctypes.c_char_p, "")
    should_kill = Value("b", False)

    @app.route("/callback", methods=["GET"])
    def callback():
        nonlocal code, should_kill
        code.value = request.args.get("code") or ""
        should_kill.value = code.value != ""
        return "Done"

    server.start()

    while not should_kill.value:
        await asyncio.sleep(1)

    server.terminate()
    server.join()

    return code.value


async def main():
    """
    The main function.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Stdout
    ------
    The code.
    """
    code = await get_code()
    print(code)

if __name__ == "__main__":
    asyncio.run(main())
