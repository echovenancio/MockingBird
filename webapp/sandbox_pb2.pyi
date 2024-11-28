from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SolutionRequest(_message.Message):
    __slots__ = ("testPath", "solution")
    TESTPATH_FIELD_NUMBER: _ClassVar[int]
    SOLUTION_FIELD_NUMBER: _ClassVar[int]
    testPath: str
    solution: str
    def __init__(
        self, testPath: _Optional[str] = ..., solution: _Optional[str] = ...
    ) -> None: ...

class SolutionReply(_message.Message):
    __slots__ = ("code", "result")
    CODE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    code: int
    result: str
    def __init__(
        self, code: _Optional[int] = ..., result: _Optional[str] = ...
    ) -> None: ...
