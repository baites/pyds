"""Generalize build-in exceptions to support data structure."""


class PydsError(Exception):
    """Base class for exceptions in this module."""
    pass


class EmptyList(PydsError):
    """Empty list exception."""
    pass
