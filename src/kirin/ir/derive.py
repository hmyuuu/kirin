from dataclasses import dataclass, field as field
from typing import Callable, Type, TypeVar

from typing_extensions import dataclass_transform

DeriveType = TypeVar("DeriveType")


@dataclass_transform()
def derive(
    cls=None,
    id_hash: bool = False,
    init: bool = False,
    repr: bool = False,
    frozen: bool = False,
) -> Callable[[Type[DeriveType]], Type[DeriveType]]:

    def wrap(cls: Type[DeriveType]):
        cls = dataclass(init=init, repr=repr, frozen=frozen)(cls)
        if id_hash:
            setattr(cls, "__hash__", lambda self: id(self))
            setattr(cls, "__eq__", lambda self, other: self is other)

        return cls

    if cls is None:
        return wrap

    return wrap(cls)
