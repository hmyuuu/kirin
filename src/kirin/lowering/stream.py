import ast
from dataclasses import dataclass, field
from typing import Sequence


@dataclass
class StmtStream:
    stmts: list[ast.stmt] = field(default_factory=list)
    cursor: int = 0

    def __init__(self, stmts: Sequence[ast.stmt], cursor: int = 0):
        self.stmts = list(stmts)
        self.cursor = cursor

    def __iter__(self):
        return self

    def __next__(self):
        if self.cursor < len(self.stmts):
            stmt = self.stmts[self.cursor]
            self.cursor += 1
            return stmt
        else:
            raise StopIteration

    def peek(self):
        return self.stmts[self.cursor]

    def has_next(self):
        return self.cursor < len(self.stmts)

    def split(self) -> "StmtStream":
        cursor = self.cursor
        self.cursor = len(self.stmts)
        return StmtStream(self.stmts, cursor)

    def __len__(self):
        return len(self.stmts)

    def __getitem__(self, key):
        return self.stmts[key]

    def __setitem__(self, key, value):
        self.stmts[key] = value

    def pop(self):
        stmt = self.stmts[self.cursor]
        self.cursor += 1
        return stmt

    def is_empty(self):
        return self.cursor == len(self.stmts)
