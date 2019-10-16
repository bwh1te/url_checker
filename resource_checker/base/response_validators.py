from abc import abstractmethod, ABC

from .exceptions import UnexpectedResponse
from .types import AnyResponse


class ResponseValidatorBase(ABC):

    def __init__(self):
        self.validation_steps = [
            self._input_validation,
            self._validate_response,
        ]

    # TODO: Docstring for ResponseValidatorBase.__call__
    def __call__(self, response: AnyResponse) -> None:
        """
        Runs all predefined checks for given `response`: preliminary response check and main
        response validation rules by default.

        :param response: Response object with requests.(get|head|...) compatible interface
        :return: None if `response` object passes all checks
        :raises: ResponseValidationFailure, UnexpectedResponse
        """
        for val_func in self.validation_steps:
            val_func(response)

    def _input_validation(self, response: AnyResponse) -> None:
        """
        Rules to preliminary check if `response` object satisfies some requirements, in other
        word, if `response` is the object we expected. For example we can check if `response`
        is actually `AnyType` instance. Or if it came right from HEAD request but not GET.

        :param response: Response object with requests.(get|head|...) compatible interface
        :return: None if `response` object has expected format
        :raises: UnexpectedResponse if something wrong with incoming `response` object
        """
        if not isinstance(response, AnyResponse):
            raise UnexpectedResponse(f'`response` parameter should be one of Response type'
                                     f' defined in `AnyResponse` but {type(response)} received')

    @abstractmethod
    def _validate_response(self, response: AnyResponse) -> None:
        """
        Defines what to check in `response` of expected format. For example you can check
        if `response` has specified headers.

        :param response: Response object with requests.(get|head|...) compatible interface
        :return: None if `response` object passes all checks
        :raises: ResponseValidationFailure if `response` validation fails
        """
        raise NotImplementedError


class HeadResponseValidatorBase(ResponseValidatorBase, ABC):
    """
    Validator for HEAD responses only.
    """

    def _input_validation(self, response: AnyResponse) -> None:
        super()._input_validation(response)
        if not self._is_head_response(response):
            raise UnexpectedResponse(f'`response` object should be a response from HEAD request')

    @abstractmethod
    def _is_head_response(self, response: AnyResponse) -> bool:
        raise NotImplementedError
