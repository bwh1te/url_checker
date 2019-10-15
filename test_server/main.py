import logging


from argparse import Namespace

from aiohttp import web
from test_server.routes import setup_routes


def create_app() -> web.Application:
    app = web.Application()
    setup_routes(app)
    return app


def main(args: Namespace) -> None:
    logging.basicConfig(level=logging.INFO)
    app = create_app()
    web.run_app(app, host=args.hostname, port=args.port)
