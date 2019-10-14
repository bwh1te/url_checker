from abc import ABC

import requests

from resource_checker.base.exceptions import ResponseValidationFailure
from resource_checker.base.response_validators import HeadResponseValidatorBase


class SimpleHeadResponseValidatorBase(HeadResponseValidatorBase, ABC):

    def _is_head_response(self, response: requests.models.Response) -> bool:
        return response.request.method == 'HEAD'


class NoChunkedHeader(SimpleHeadResponseValidatorBase):
    # TODO: Docstring for NoChunkedHeader class - explain why we need it

    def validate_response(self, response: requests.Session):
        if response.headers.get('Transfer-Encoding') == 'chunked':
            raise ResponseValidationFailure('Validation failed: found Transfer-Encoding '
                                            'header set to `chunked`')


class HasContentLengthHeader(SimpleHeadResponseValidatorBase):
    # TODO: Docstring for HasContentLengthHeader class - explain why we need it

    def validate_response(self, response: requests.Session):
        has_content_length = response.headers.get('Content-Length')
        if not has_content_length:
            raise ResponseValidationFailure('Validation failed: no Content-Length header')
