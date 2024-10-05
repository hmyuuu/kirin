from kirin.decl import info, statement
from kirin.dialects.cf.dialect import dialect
from kirin.dialects.py.types import Bool, String
from kirin.ir import Block, IsTerminator, SSAValue, Statement
from kirin.print.printer import Printer


@statement(dialect=dialect)
class Assert(Statement):
    name = "assert"
    traits = frozenset({})

    condition: SSAValue
    message: SSAValue = info.argument(String)


@statement(dialect=dialect)
class Branch(Statement):
    name = "br"
    traits = frozenset({IsTerminator()})

    arguments: tuple[SSAValue, ...]
    successor: Block = info.block()

    def print_impl(self, printer: Printer) -> None:
        with printer.rich(style="red"):
            printer.print_str(self.name)
        printer.print_str(" ")
        printer.print_str(printer.block.get_name(self.successor))
        printer.print_str("(")
        printer.show_list(self.arguments)
        printer.print_str(")")


@statement(dialect=dialect)
class ConditionalBranch(Statement):
    name = "cond_br"
    traits = frozenset({IsTerminator()})

    cond: SSAValue = info.argument(Bool)
    then_arguments: tuple[SSAValue, ...]
    else_arguments: tuple[SSAValue, ...]

    then_successor: Block = info.block()
    else_successor: Block = info.block()

    def print_impl(self, printer: Printer) -> None:
        with printer.rich(style="red"):
            printer.print_str(self.name)
        printer.print_str(" ")
        self.cond.print_impl(printer)

        with printer.rich(style="black"):
            printer.print_str(" goto ")

        printer.print_str(printer.block.get_name(self.then_successor))
        printer.print_str("(")
        printer.show_list(self.then_arguments)
        printer.print_str(")")
        with printer.rich(style="black"):
            printer.print_str(" else ")
        printer.print_str(printer.block.get_name(self.else_successor))
        printer.print_str("(")
        printer.show_list(self.else_arguments)
        printer.print_str(")")
