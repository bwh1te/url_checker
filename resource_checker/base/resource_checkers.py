from abc import ABC, abstractmethod
from typing import Optional, Sequence, Type

from resource_checker.base.exceptions import (
    RequesterProcessingFailure,
    ResponseValidationFailure,
)

from .response_validators import HeadResponseValidatorBase
from .requesters import RequesterBase


class ResourceCheckerBase(ABC):

    def __init__(self,
                 head_requester: Type[RequesterBase] = None,
                 head_validators: Sequence[Type[HeadResponseValidatorBase]] = None):
        self._head_requester = head_requester()
        self._head_validators = [c() for c in head_validators]

    def __call__(self, url: str) -> Optional[str]:
        try:
            head_response = self._head_requester.make_request(url)
        except RequesterProcessingFailure:
            return None

        real_url = head_response.url

        for validator_func in self._head_validators:
            try:
                validator_func(head_response)
            except ResponseValidationFailure:
                return None

        return real_url

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError
