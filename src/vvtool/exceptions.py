"""Custom exceptions for the module."""


class VoteviewException(Exception):
    """Base class for all Voteview exceptions."""


class DuplicateError(VoteviewException):
    """The value is a duplicate."""


class MissingReferent(VoteviewException):
    """The value is missing a referent."""


class NotFound(VoteviewException):
    """No match was found."""
