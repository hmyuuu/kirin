from kirin.decl import info, statement
from kirin.dialects.py import data, types
from kirin.dialects.py.stmts.dialect import dialect
from kirin.ir import Pure, ResultValue, SSAValue, Statement
from kirin.print.printer import Printer

T = types.PyTypeVar("T")


@statement(dialect=dialect)
class Alias(Statement):
    name = "alias"
    traits = frozenset({Pure()})
    value: SSAValue = info.argument(T)
    target: data.PyAttr[str] = info.attribute(property=True)
    result: ResultValue = info.result(T)

    def print_impl(self, printer: Printer) -> None:
        printer.show_name(self)
        printer.print_str(" ")
        with printer.rich(style="yellow"):
            printer.print_str(self.target.data)
        with printer.rich(style="red"):
            printer.print_str(" = ")
        self.value.print_impl(printer)
