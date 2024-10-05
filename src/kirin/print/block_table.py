from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kirin.ir import Block


@dataclass
class BlockTable:
    block_names: dict[Block, int] = field(default_factory=dict)
    next_id: int = 0

    def get_name(self, block: Block) -> str:
        if block in self.block_names:
            name = self.block_names[block]
        else:
            name = self.next_id
            self.next_id += 1
            self.block_names[block] = name

        return f"^{name}"
