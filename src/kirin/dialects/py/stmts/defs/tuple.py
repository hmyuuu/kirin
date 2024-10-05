from kirin.decl import info, statement
from kirin.dialects.py import types
from kirin.dialects.py.stmts.dialect import dialect
from kirin.ir import ResultValue, SSAValue, Statement
from kirin.print.printer import Printer


@statement(dialect=dialect)
class NewTuple(Statement):
    result: ResultValue = info.result()

    def __init__(self, values: tuple[SSAValue, ...]) -> None:
        result_type = types.PyGeneric(tuple, *tuple(value.type for value in values))  # type: ignore
        super().__init__(
            args=values,
            result_types=[
                result_type,
            ],
        )

    def print_impl(self, printer: Printer) -> None:
        printer.show_name(self)
        printer.print_str("(")
        printer.show_list(self.args, delim=", ")
        printer.print_str(")")

        with printer.rich(style="black"):
            printer.print_str(" -> ")
            printer.print(self.result.type)
