from typing import Callable, Optional, Sequence, Type

import requests

from resource_checker.base.exceptions import ResourceCheckerConfigurationError
from resource_checker.base.resource_checkers import ResourceCheckerBase
from resource_checker.base.url_validators import has_no_redirects

from .requesters import SessionBasedHeadRequester
from .response_validators import (
    HasContentLengthHeader,
    HttpStatusIsOk,
    NoChunkedHeader,
    SimpleHeadResponseValidatorBase,
)


class SessionBasedResourceChecker(ResourceCheckerBase):
    """
    Resource Checker realization, which uses `requests` module to work with urls.
    """

    def __init__(self,
                 url_validators: Sequence[Callable[[str], bool]] = None,
                 head_requester: Type[SessionBasedHeadRequester] = None,
                 head_validators: Sequence[Type[SimpleHeadResponseValidatorBase]] = None):

        # Set default requester and validators if custom are not provided
        url_validators = url_validators or [
            has_no_redirects,
        ]
        head_requester = head_requester or SessionBasedHeadRequester
        head_validators = head_validators or [
            HttpStatusIsOk,
            HasContentLengthHeader,
            NoChunkedHeader,
        ]

        super().__init__(url_validators, head_requester, head_validators)
        self._session = None

    def __enter__(self):
        self._session = requests.Session()
        self._session.max_redirects = 20
        self._head_requester.set_session(self._session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()
        self._session = None

    def __call__(self, url: str) -> Optional[str]:
        if not hasattr(self, '_session'):
            raise ResourceCheckerConfigurationError('You should set _session before calling '
                                                    'SessionBasedResourceChecker instance')
        return super().__call__(url)
