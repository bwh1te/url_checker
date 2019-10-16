"""
Integrity tests to check how SessionBasedResourceChecker works in common.

Uses `test_server` module to emulate different problems on retrieving url content.

"""

import urllib.parse

import pytest

from resource_checker.base.exceptions import ResourceCheckerValidationFailure


@pytest.mark.parametrize("input_path,expected_path", [
    ('/good_one', '/good_one'),
    ('/redirect_single', '/good_one'),
    ('/redirect_multi/5', '/good_one'),
])
def test_resource_checker_call_valid(run_local_server,
                                     session_based_resource_checker,
                                     input_path,
                                     expected_path):
    """
    Checks test server's `input_path` with SessionBasedResourceChecker instance.
    Test for positive cases:
        /good_one - just responses with 200 Ok
        /redirect_single - redirects to /good_one
        /redirect_multi/5 - chain of redirects leads to /good_one

    :param run_local_server: fixture to start `test_server` locally
    :param session_based_resource_checker: fixture to init SessionBasedResourceChecker
    :param input_path: path to check on `test_server`
    :param expected_path: path to `test_server` where `input_path` leads after all redirects
    """
    result_url = session_based_resource_checker(
        urllib.parse.urljoin(run_local_server, input_path)
    )
    parsed_result_url = urllib.parse.urlparse(result_url)
    assert parsed_result_url.path == expected_path


@pytest.mark.parametrize("input_path", [
    '/redirect_infinite',
    '/redirect_cycle/a',
    '/chunked',
    '/404_not_found',
])
def test_resource_checker_call_invalid(run_local_server,
                                       session_based_resource_checker,
                                       input_path):
    """
    Checks test server's `input_path` with SessionBasedResourceChecker instance.
    Test for negative cases:
        /redirect_infinite - cyclic redirect to the same url
        /redirect_cycle/a - cyclic redirect through the chain of urls (a -> b -> c -> d -> a)
        /chunked - response with transfer-encoding: chunked
        /404_not_found - not found

    :param run_local_server: fixture to start `test_server` locally
    :param session_based_resource_checker: fixture to init SessionBasedResourceChecker
    :param input_path: path to check on `test_server`
    """
    with pytest.raises(ResourceCheckerValidationFailure):
        _ = session_based_resource_checker(
            urllib.parse.urljoin(run_local_server, input_path)
        )
