from kirin.decl import info, statement
from kirin.dialects.py import types
from kirin.dialects.py.stmts.dialect import dialect
from kirin.ir import Pure, ResultValue, SSAValue, Statement
from kirin.print.printer import Printer


@statement(dialect=dialect)
class NewList(Statement):
    name = "list"
    traits = frozenset({Pure()})

    def __init__(self, type: types.PyType, values: tuple[SSAValue, ...]) -> None:
        super().__init__(
            args=values,
            result_types=[
                types.List[type],
            ],
        )

    def print_impl(self, printer: Printer) -> None:
        printer.show_name(self)
        printer.print_str("(")
        printer.show_list(self.args)
        printer.print_str(")")
        with printer.rich(style="black"):
            printer.print_str(" : ")
            printer.show_function_types(
                [arg.type for arg in self.args],
                [result.type for result in self._results],
            )


@statement(dialect=dialect)
class Append(Statement):
    name = "append"
    traits = frozenset({})
    lst: SSAValue = info.argument(types.List)
    value: SSAValue = info.argument(types.Any)


@statement(dialect=dialect)
class Len(Statement):
    name = "len"
    traits = frozenset({Pure()})
    value: SSAValue = info.argument(types.Any)
    result: ResultValue = info.result(types.Int)
