"""
Unit tests to check Requesters (e.g. SessionBasedHeadRequester) separately.

This is far from complete coverage, but it is more an example to show other concepts different
from the integrity testing approach used in `test_resource_checkers.py`. Instead of using real
server to emulate corner cases, we mock responses that `requester` object receives. It has
`requests` under the hood, so we can mock `requests` functions like `head` or `get`. Or use
`responses` library that does the same.

"""

import responses
import requests

from resource_checker.simple_checker.requesters import SessionBasedHeadRequester


def test_request_good_url():
    url = 'http://localhost:8080/good_one'
    with responses.RequestsMock() as fake_response:
        fake_response.add(fake_response.HEAD, url, status=200)

        head_requester = SessionBasedHeadRequester()
        head_requester.set_session(
            requests.Session()
        )
        head_response = head_requester.make_request('http://localhost:8080/good_one')

        assert head_response.status_code == 200


def test_request_redirect_single():
    with responses.RequestsMock() as fake_response:
        fake_response.add(
            fake_response.HEAD,
            'http://localhost:8080/redirect_single',
            status=301,
            headers={
                'Location': '/good_one'
            }
        )
        fake_response.add(
            fake_response.HEAD,
            'http://localhost:8080/good_one',
            status=200
        )

        head_requester = SessionBasedHeadRequester()
        head_requester.set_session(
            requests.Session()
        )
        head_response = head_requester.make_request('http://localhost:8080/redirect_single')

        assert head_response.status_code == 200
