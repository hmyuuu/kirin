from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from kirin.ir import DialectGroup, Method


@dataclass
class Pass(ABC):
    name: ClassVar[str]
    dialects: DialectGroup

    @abstractmethod
    def __call__(self, mt: Method) -> None: ...
