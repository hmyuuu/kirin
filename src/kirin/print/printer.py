from __future__ import annotations

import io
from dataclasses import dataclass, field
from typing import IO, TYPE_CHECKING, Callable, Generic, Iterable, Sequence, TypeVar

from rich.console import Console

from kirin.print.block_table import BlockTable
from kirin.print.printable import Printable
from kirin.print.ssa_table import SSAValueTable

if TYPE_CHECKING:
    from types import ModuleType

    from kirin.ir import Attribute, ResultValue, Statement, TypeAttribute


@dataclass
class PrintOptions:
    show_block_args: bool = True
    show_block_terminator: bool = True
    show_indent_mark: bool = True


IOType = TypeVar("IOType", bound=IO)
OtherIOType = TypeVar("OtherIOType", bound=IO)


@dataclass
class Printer(Generic[IOType]):
    console: Console = field(default_factory=Console)
    ssa: SSAValueTable = field(default_factory=SSAValueTable, repr=False)
    block: BlockTable = field(default_factory=BlockTable, repr=False)

    # print state
    _indent: int = field(default=0, repr=False)
    _indent_marks: list[int] = field(default_factory=list, repr=False)

    _result_width: int = field(default=0, repr=False)
    _current_line: int = field(default=0, repr=False)
    _current_column: int = field(default=0, repr=False)
    _messages: list[str] = field(default_factory=list, repr=False)
    _print_function_types: bool = field(default=True, repr=False)

    # rich style
    _style: str | None = field(default=None, repr=False)
    _highlight: bool = field(default=False, repr=False)

    # print options
    options: PrintOptions = field(default_factory=PrintOptions)

    def similar(self, stream: OtherIOType | None = None) -> Printer[OtherIOType]:
        return Printer(
            console=Console(file=stream),
            ssa=self.ssa,
            block=self.block,
            _indent=self._indent,
            _current_line=self._current_line,
            _current_column=self._current_column,
            _messages=self._messages,
            options=self.options,
        )

    def print(self, *args) -> None:
        # TODO: support dataclass printing
        for each in args:
            if isinstance(each, Printable):
                each.print_impl(self)
            elif hasattr(self, "print_" + type(each).__name__):
                getattr(self, "print_" + type(each).__name__)(each)
            else:
                raise ValueError(f"Cannot print {type(each).__name__}")

    def print_module(self, obj: ModuleType):
        self.print_str(f"Module({obj.__name__})")

    def print_str(self, text: str):
        lines = text.split("\n")
        if len(lines) != 1:
            self._current_line += len(lines) - 1
            self._current_column = len(lines[-1])
        else:
            self._current_column += len(lines[-1])
        self.console.print(text, end="", style=self._style, highlight=self._highlight)

    def print_int(self, obj: int):
        self.print_str(str(obj))

    def print_float(self, obj: float):
        self.print_str(str(obj))

    def print_tuple(self, obj: tuple):
        self.print_str("(")
        self.show_list(obj, lambda x: self.print_str(repr(x)))
        if len(obj) == 1:
            self.print_str(",")
        self.print_str(")")

    def print_list(self, obj: list):
        self.print_str("[")
        self.show_list(obj, self.print)
        self.print_str("]")

    def print_dict(self, obj: dict):
        self.print_str("{")
        self.show_dict(obj, self.print)
        self.print_str("}")

    def newline(self) -> None:
        self.only_newline()

        if self._messages:
            for message in self._messages:
                self.print_str(message)
                self.only_newline()
                self.only_indent()
            self._messages.clear()
        else:
            self.only_indent()

    def only_newline(self) -> None:
        self.print_str("\n")
        self._current_line += 1
        self._current_column = 0

    def only_indent(self) -> None:
        indent_str = ""
        if self.options.show_indent_mark and self._indent_marks:
            indent_marks = self._indent_marks + [self._indent]
            diff = [j - i - 1 for i, j in zip(indent_marks, indent_marks[1:])]
            indent_str = "│".join([" " * w for w in [0] + diff])

            with self.rich(style="bright_black"):
                self.print_str(indent_str)
        else:
            indent_str = " " * self._indent
            self.print_str(indent_str)

    # utility functions (marked with show_ prefix)
    ElemType = TypeVar("ElemType")

    def show_list(
        self,
        elems: Iterable[ElemType],
        print_fn: Callable[[ElemType], None] | None = None,
        delim: str = ", ",
        prefix: str = "",
        suffix: str = "",
    ) -> None:
        print_fn = print_fn or self.print

        self.print_str(prefix)
        for i, elem in enumerate(elems):
            if i > 0:
                self.print(delim)
            print_fn(elem)
        self.print_str(suffix)

    KeyType = TypeVar("KeyType")
    ValueType = TypeVar("ValueType")

    def show_dict(
        self,
        elems: dict[KeyType, ValueType],
        print_fn: Callable[[ValueType], None] | None = None,
        delim: str = ", ",
    ) -> None:
        print_fn = print_fn or self.print
        for i, (key, value) in enumerate(elems.items()):
            if i > 0:
                self.print_str(delim)
            self.print_str(f"{key}=")
            print_fn(value)

    def result_str(self, results: list[ResultValue]) -> str:
        stream = io.StringIO()
        str_print = self.similar(stream)
        str_print.show_list(results, str_print.print)
        result_str = stream.getvalue()
        stream.close()
        return result_str

    def result_len(self, results: list[ResultValue]) -> int:
        return len(self.result_str(results))

    def show_results(self, results: list[ResultValue]) -> None:
        if results:
            result_str = self.result_str(results)
            self.print_str(result_str.rjust(self._result_width))
            self.print(" = ")
        elif self._result_width:
            self.print(" ".rjust(self._result_width) + "   ")
        else:  # no width, e.g module
            return

    def show_stmts(self, stmts: Iterable[Statement]) -> None:
        result_strlen = [self.result_len(stmt._results) for stmt in stmts]
        with self.align_result(max(result_strlen) if result_strlen else 0):
            with self.indent(increase=2, mark=True):
                for idx, stmt in enumerate(stmts):
                    self.newline()
                    self.show_results(stmt._results)
                    stmt.print_impl(self)

    def show_function_types(
        self, input_types: Sequence[TypeAttribute], output_type: Sequence[TypeAttribute]
    ) -> None:
        from kirin.dialects.func.attrs import Signature

        self.print_str("(")
        self.show_list(input_types)
        self.print_str(") -> ")
        if len(output_type) == 1:
            output_type_0 = output_type[0]
            if isinstance(output_type_0, Signature):
                self.print_str("(")
                output_type_0.print(self)
                self.print_str(")")
            else:
                output_type_0.print_impl(self)
        else:
            self.print_str("(")
            self.show_list(output_type)
            self.print_str(")")

    def show_name(self, node: Attribute | Statement, prefix: str = "") -> None:
        return self.show_dialect_path(node, node.name, prefix=prefix)

    def show_dialect_path(
        self, node: Attribute | Statement, text: str, prefix: str = ""
    ) -> None:
        if node.dialect:  # not None
            self.print_str(prefix)
            with self.rich(style="dark_blue"):
                self.print_str(f"{node.dialect.name}.")
        else:
            self.print_str(prefix)
        self.print_str(text)

    def indent(self, increase: int = 2, mark: bool = False) -> NewIndent:
        return NewIndent(self, increase, mark)

    def align_result(self, width: int) -> AlignResult:
        return AlignResult(self, width)

    def rich(self, **kw) -> RichOption:
        return RichOption(self, **kw)

    def debug(self, msg: str) -> None:
        self._messages.append(f"DEBUG: {msg}")


@dataclass
class NewIndent:
    printer: Printer
    increase: int = 2
    mark: bool = False

    def __enter__(self):
        if self.mark:
            self.printer._indent_marks.append(self.printer._indent)
        self.printer._indent += self.increase

    def __exit__(self, exc_type, exc_value, traceback):
        self.printer._indent -= self.increase
        if self.mark:
            self.printer._indent = self.printer._indent_marks.pop()
        return False


@dataclass
class AlignResult:
    printer: Printer
    previous_width: int
    current_width: int

    def __init__(self, printer: Printer, width: int):
        self.printer = printer
        self.previous_width = printer._result_width
        self.current_width = width

    def __enter__(self):
        self.printer._result_width = self.current_width

    def __exit__(self, exc_type, exc_value, traceback):
        self.printer._result_width = self.previous_width
        return False


@dataclass
class RichOption:
    printer: Printer
    style: str | None = None
    highlight: bool = False

    def __enter__(self):
        self.printer._style, self.style = self.style, self.printer._style
        self.printer._highlight, self.highlight = (
            self.highlight,
            self.printer._highlight,
        )

    def __exit__(self, exc_type, exc_value, traceback):
        self.printer._style = self.style
        self.printer._highlight = self.highlight
        return False
