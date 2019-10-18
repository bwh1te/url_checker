"""
Exceptions used in resource_checker module.

Exception hierarchy:

    ResourceCheckerError
        ResourceCheckerConfigurationError
        ResourceCheckerValidationFailure

    RequesterError
        RequesterConfigurationError
        RequesterProcessingFailure

    ResponseValidatorError
        UnexpectedResponse
        ResponseValidationFailure

    UrlValidationFailure

"""


class ResourceCheckerError(Exception):
    """
    Base class for Exceptions raises by ResourceCheckerBase successors.
    """
    pass


class ResourceCheckerConfigurationError(ResourceCheckerError):
    """
    Raises in case of ResourceCheckerBase successor improper configuration.
    """
    pass


class ResourceCheckerValidationFailure(ResourceCheckerError):
    """
    Raises if resource validation was failed.
    """
    pass


class RequesterError(Exception):
    """
    Base class for Exceptions raises by RequesterBase successors.
    """
    pass


class RequesterConfigurationError(RequesterError):
    """
    Raises in case of RequesterBase successor improper configuration.
    """
    pass


class RequesterProcessingFailure(RequesterError):
    """
    Raises if an error occurred in RequesterBase successor while requesting for a resource.
    """
    pass


class ResponseValidatorError(Exception):
    """
    Base class for Exceptions raises by ResponseValidatorBase successors.
    """
    pass


class UnexpectedResponse(ResponseValidatorError):
    """
    Raises if ResponseValidator received unexpected Response.
    """
    pass


class ResponseValidationFailure(ResponseValidatorError):
    """
    Raises if Response didn't pass validation.
    """
    pass


class UrlValidationFailure(Exception):
    """
    Raises in case of bad url
    """
    pass