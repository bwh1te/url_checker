from typing import Union

import requests


# Classes which `Response` instance (uses by Response Validators) actually could be.
# Each of them should implement the same interface as `request.models.Response` or
# `aiohttp.client_reqrep.ClientResponse`. In particular it should provide access to
# it's headers dict, request object and request's object method at least.
# TODO: Maybe it could be better not to bring any info about implementation dependencies to the base-level  # noqa: E501
AnyResponse = Union[requests.models.Response, ]
