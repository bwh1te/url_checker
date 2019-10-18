from abc import ABC, abstractmethod
from typing import Callable, Optional, Sequence, Type

from resource_checker.base.exceptions import (
    RequesterProcessingFailure,
    ResourceCheckerValidationFailure,
    ResponseValidationFailure,
    UrlValidationFailure,
)

from .response_validators import HeadResponseValidatorBase
from .requesters import RequesterBase


class ResourceCheckerBase(ABC):
    """
    Base class to inherit Resource Checkers from.

    Key idea is to make HEAD request to target url and to make decision about this resource
    based on response. Whilst the overall pipeline design is predefined in base class, logic
    of each step is defined inside Requester's and Validators' classes provided during
    the initialization.
    """

    def __init__(self,
                 url_validators: Sequence[Callable[[str], None]],
                 head_requester: Type[RequesterBase],
                 head_validators: Sequence[Type[HeadResponseValidatorBase]]):
        self._url_validators = url_validators
        self._head_requester = head_requester()
        self._head_validators = [c() for c in head_validators]

    def __call__(self, url: str) -> Optional[str]:
        """
        Finds the final resource destination where `url` leads to after all redirects.

        :param url: URL to check
        :return: final resource location after all redirects
        :raises: ResourceCheckerError
        """

        # Checking the url string before trying to make requests
        for url_validator_func in self._url_validators:
            try:
                url_validator_func(url)
            except UrlValidationFailure as e:
                raise ResourceCheckerValidationFailure(str(e))

        try:
            head_response = self._head_requester.make_request(url)
        except RequesterProcessingFailure as e:
            raise ResourceCheckerValidationFailure(str(e))

        real_url = head_response.url

        for validator_func in self._head_validators:
            try:
                validator_func(head_response)
            except ResponseValidationFailure as e:
                raise ResourceCheckerValidationFailure(str(e))

        return real_url

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError
