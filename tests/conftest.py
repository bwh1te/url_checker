import subprocess
import time

import pytest

from resource_checker.simple_checker.resource_checkers import SessionBasedResourceChecker
from resource_checker.simple_checker.requesters import SessionBasedHeadRequester
from resource_checker.simple_checker.response_validators import (
    HasContentLengthHeader,
    NoChunkedHeader,
)

TEST_SERVER_HOST = 'localhost'
TEST_SERVER_PORT = '8080'


@pytest.fixture(scope='session')
def run_local_server() -> str:
    """
    Runs separate process with test_server application, which emulates possible cases
    that resource_checkers should detect.

    :return str: base url where test_server listens. We need it to build expected urls properly.
    """
    proc = subprocess.Popen(
        ['python', '-m', 'test_server', '-H', TEST_SERVER_HOST, '-P', TEST_SERVER_PORT],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(3)  # TODO: Wait while test_server starts for real
    yield f'http://{TEST_SERVER_HOST}:{TEST_SERVER_PORT}'
    proc.kill()


@pytest.fixture(scope='session')
def session_based_resource_checker():
    """
    Creates SessionBasedResourceChecker instance and starts context for it.
    """
    with SessionBasedResourceChecker(
        head_requester=SessionBasedHeadRequester,
        head_validators=[HasContentLengthHeader, NoChunkedHeader]
    ) as checker:
        yield checker
