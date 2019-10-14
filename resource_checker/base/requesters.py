from abc import ABC, abstractmethod

from .types import AnyResponse


class RequesterBase(ABC):

    @abstractmethod
    def make_request(self, url: str) -> AnyResponse:
        """
        Makes request to `url`. Any additional settings should be set whilst obj initiation.
        :param url: URL to request
        :return: response object
        :raises: RequesterConfigurationError, RequesterProcessingFailure
        """
        raise NotImplementedError
