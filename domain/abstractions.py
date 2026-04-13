from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

@dataclass(frozen=True)
class Error:
    code: str
    description: str
    status_code: int

NONE_ERROR = Error(code="", description="", status_code=200)

class Result(Generic[T]):
    """Result Pattern implementation in Python"""
    def __init__(self, is_success: bool, error: Error, value: Optional[T] = None):
        if is_success and error != NONE_ERROR:
            raise ValueError("Success result cannot have an error.")
        if not is_success and error == NONE_ERROR:
            raise ValueError("Failure result must have an error.")

        self.is_success = is_success
        self.is_failure = not is_success
        self.error = error
        self._value = value

    @property
    def value(self) -> T:
        if self.is_failure:
            raise ValueError("Failure results cannot have a value.")
        return self._value # type: ignore

    @classmethod
    def success(cls, value: Optional[T] = None) -> 'Result[T]':
        return cls(is_success=True, error=NONE_ERROR, value=value)

    @classmethod
    def failure(cls, error: Error) -> 'Result[T]':
        return cls(is_success=False, error=error, value=None)

# Exception wrapper to trigger the ProblemDetails response in FastAPI
class ResultException(Exception):
    def __init__(self, error: Error):
        self.error = error