import logging


from argparse import Namespace

from aiohttp import web
from server.routes import setup_routes


def main(args: Namespace):
    logging.basicConfig(level=logging.INFO)
    app = web.Application()
    setup_routes(app)
    web.run_app(app, host=args.hostname, port=args.port)
