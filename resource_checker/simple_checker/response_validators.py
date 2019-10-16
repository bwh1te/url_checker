from abc import ABC

import requests

from resource_checker.base.exceptions import ResponseValidationFailure
from resource_checker.base.response_validators import HeadResponseValidatorBase


class SimpleHeadResponseValidatorBase(HeadResponseValidatorBase, ABC):

    def _is_head_response(self, response: requests.models.Response) -> bool:
        return response.request.method == 'HEAD'


class HttpStatusIsOk(SimpleHeadResponseValidatorBase):
    """
    First of all, we consider url good if it responses with 200 Ok
    """

    def _validate_response(self, response: requests.models.Response) -> None:
        if response.status_code != 200:
            raise ResponseValidationFailure(f'{response.request.url} Validation failed: '
                                            f'response must be 200 Ok but it is '
                                            f'{response.status_code} {response.reason}')


class NoChunkedHeader(SimpleHeadResponseValidatorBase):
    """
    Resource with `Transfer-encoding: chunked header` could probably has unlimited length.
    """

    def _validate_response(self, response: requests.models.Response) -> None:
        if response.headers.get('Transfer-Encoding') == 'chunked':
            raise ResponseValidationFailure(f'{response.request.url} Validation failed: '
                                            f'found Transfer-Encoding header set to `chunked`')


class HasContentLengthHeader(SimpleHeadResponseValidatorBase):
    """
    Resource with no `Content-Length` header is suspicious too. Most of clients relies on this
    information when reading content.
    """

    def _validate_response(self, response: requests.models.Response) -> None:
        has_content_length = response.headers.get('Content-Length')
        if not has_content_length:
            raise ResponseValidationFailure(f'{response.request.url} Validation failed: '
                                            f'no Content-Length header')
