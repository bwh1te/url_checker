import argparse

from test_server.main import main


parser = argparse.ArgumentParser(description="Run a simple HTTP server")
parser.add_argument(
    "-H",
    "--hostname",
    default="localhost",
    help="TCP/IP hostname to serve on (default: %(default)r)",
)
parser.add_argument(
    "-P",
    "--port",
    type=int,
    default=8080,
    help="TCP/IP port to serve on (default: %(default)r)",
)
args = parser.parse_args()

main(args)
