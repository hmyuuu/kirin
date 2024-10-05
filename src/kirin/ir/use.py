from __future__ import annotations

from typing import TYPE_CHECKING

from kirin.ir.derive import derive

if TYPE_CHECKING:
    from kirin.ir.nodes.stmt import Statement


@derive(init=True, repr=True, frozen=True)
class Use:
    stmt: Statement
    index: int
