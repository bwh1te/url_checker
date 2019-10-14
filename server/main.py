import logging


from argparse import Namespace

from aiohttp import web
from server.routes import setup_routes


def create_app():
    app = web.Application()
    setup_routes(app)
    return app


def main(args: Namespace):
    logging.basicConfig(level=logging.INFO)
    app = create_app()
    web.run_app(app, host=args.hostname, port=args.port)
