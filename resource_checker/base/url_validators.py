"""
Simple functions to check the STRING form of URL _BEFORE_ making any requests to it.

For example if given string is valid URL, or maybe to check if URL don't leads
to domain from ban-list.
"""

import re

from .exceptions import UrlValidationFailure


def has_no_redirects(url: str):
    https_found = re.findall(r'https?://', url)
    if len(https_found) > 1:
        raise UrlValidationFailure(f'{url} Potentially has redirect')
