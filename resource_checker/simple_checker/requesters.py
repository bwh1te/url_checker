from abc import ABC

import requests
from requests.exceptions import TooManyRedirects

from resource_checker.base.exceptions import (
    RequesterConfigurationError,
    RequesterProcessingFailure,
)
from resource_checker.base.requesters import RequesterBase


class SessionBasedRequesterBase(RequesterBase, ABC):

    def __init__(self):
        self._session = None

    def set_session(self, session: requests.Session) -> None:
        self._session = session


class SessionBasedHeadRequester(SessionBasedRequesterBase):

    def make_request(self, url: str) -> requests.models.Response:
        if not self._session:
            raise RequesterConfigurationError('Improper configuration: you should set '
                                              'session first')
        try:
            with self._session.head(url, allow_redirects=True) as resp:
                return resp
        except TooManyRedirects as e:
            # Notice that maximum number of possible redirects are set outside,
            # as the incoming request.Session() object option `max_redirects`.
            raise RequesterProcessingFailure('Exceeded maximum redirect count')
