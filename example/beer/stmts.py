from attrs import Beer
from dialect import dialect

from kirin.decl import info, statement
from kirin.dialects.py import types
from kirin.ir import Block, IsTerminator, Pure, ResultValue, SSAValue, Statement


@statement(dialect=dialect)
class NewBeer(Statement):
    name = "new_beer"
    traits = frozenset({Pure()})
    brand: SSAValue = info.argument(types.String)
    result: ResultValue = info.result(types.PyClass(Beer))


@statement(dialect=dialect)
class Drink(Statement):
    name = "drink"
    beverage: SSAValue = info.argument(types.PyClass(Beer))


@statement(dialect=dialect)
class Pour(Statement):
    name = "pour"
    beverage: SSAValue = info.argument(types.PyClass(Beer))
    amount: SSAValue = info.argument(types.Int)


@statement(dialect=dialect)
class RandomBranch(Statement):
    name = "random_br"
    traits = frozenset({IsTerminator()})
    cond: SSAValue = info.argument(types.Bool)
    then_arguments: tuple[SSAValue, ...] = info.argument()
    else_arguments: tuple[SSAValue, ...] = info.argument()
    then_successor: Block = info.block()
    else_successor: Block = info.block()


@statement(dialect=dialect)
class Puke(Statement):
    name = "puke"
