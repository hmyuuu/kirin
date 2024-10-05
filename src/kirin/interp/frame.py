from dataclasses import dataclass, field
from typing import Any, Iterable

from kirin.exceptions import InterpreterError
from kirin.ir import Method, SSAValue, Statement


@dataclass
class Frame:
    method: Method
    """method being interpreted.
    """
    lino: int = 0
    stmt: Statement | None = None
    """statement being interpreted.
    """

    globals: dict[str, Any] = field(default_factory=dict)
    """Global variables this frame has access to.
    """

    # NOTE: we are sharing the same frame within blocks
    # this is because we are validating e.g SSA value pointing
    # to other blocks separately. This avoids the need
    # to have a separate frame for each block.
    entries: dict[SSAValue, Any] = field(default_factory=dict)
    """SSA values and their corresponding values.
    """

    @classmethod
    def from_method(cls, method: Method) -> "Frame":
        return cls(method=method)

    def get_values(self, keys: Iterable[SSAValue]) -> tuple:
        try:
            return tuple(self.entries[key] for key in keys)
        except KeyError as e:
            raise InterpreterError(f"SSA value {e} not found in frame")

    def set_values(self, pairs: Iterable[tuple[SSAValue, Any]]):
        for key, value in pairs:
            self.entries[key] = value
