import ctypes
import logging
import click
import typing as t

from multiprocessing import Process, Manager, Value
from flask import Flask, request
import asyncio


def flask_keep_quiet():
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
        pass

    click.echo = echo
    click.secho = echo


async def get_code(port: int = 8000) -> str:
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
    code = await get_code()
    print(code)

if __name__ == "__main__":
    asyncio.run(main())
