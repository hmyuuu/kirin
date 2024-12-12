from typing import TYPE_CHECKING, Generic, TypeVar
from dataclasses import field, dataclass

if TYPE_CHECKING:
    from kirin.ir.ssa import SSAValue


T = TypeVar("T")


@dataclass
class IdTable(Generic[T]):
    ssa_ids: dict[T, int] = field(default_factory=dict)
    next_id: int = 0

    def add(self, value: T) -> int:
        id = self.next_id
        self.ssa_ids[value] = id
        self.next_id += 1
        return id

    def __getitem__(self, value: T) -> int:
        if value in self.ssa_ids:
            return self.ssa_ids[value]
        else:
            return self.add(value)


@dataclass
class SSAValueSymbolTable:
    ssa_names: dict["SSAValue", str] = field(default_factory=dict)
    name_count: dict[str, int] = field(default_factory=dict)
    next_id: int = 0

    def get_name(self, value: "SSAValue") -> str:
        if value in self.ssa_names:
            name = self.ssa_names[value]
        elif value.name:
            curr_ind = self.name_count.get(value.name, 0)
            suffix = f"_{curr_ind}" if curr_ind != 0 else ""
            name = "%" + value.name + suffix
            self.name_count[value.name] = curr_ind + 1
            self.ssa_names[value] = name
        else:
            name = f"%{self.next_id}"
            self.next_id += 1
            self.ssa_names[value] = name

        return name
