"""
Integrity tests to check how SessionBasedResourceChecker works in common.

Uses `test_server` module to emulate different problems on retrieving url content.

"""

import urllib.parse

import pytest


@pytest.mark.parametrize("input_path,expected_path", [
    ('/good_one', '/good_one'),
    ('/redirect_single', '/good_one'),
    ('/redirect_multi/5', '/good_one'),
    ('/redirect_infinite', None),
    ('/redirect_cycle/a', None),
    ('/chunked', None),
])
def test_resource_checker_call(run_local_server,
                               session_based_resource_checker,
                               input_path,
                               expected_path):
    """
    Checks test server's `input_path` with SessionBasedResourceChecker instance.

    :param run_local_server: fixture to start `test_server` locally
    :param session_based_resource_checker: fixture to init SessionBasedResourceChecker
    :param input_path: path to check on `test_server`
    :param expected_path: path to `test_server` where `input_path` leads after all redirects
    """
    url_to_check = urllib.parse.urljoin(run_local_server, input_path)
    result_url = session_based_resource_checker(url_to_check)
    if expected_path is None:
        assert result_url is None
    else:
        parsed_result_url = urllib.parse.urlparse(result_url)
        assert parsed_result_url.path == expected_path
