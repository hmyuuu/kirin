from kirin.decl import info, statement
from kirin.dialects.py import types
from kirin.dialects.py.stmts.dialect import dialect
from kirin.ir import Pure, ResultValue, SSAValue, Statement


# NOTE: in IR setindex is very different from getindex
# taking Julia's semantics as reference here
@statement
class Subscript(Statement):
    pass


@statement(dialect=dialect)
class GetItem(Subscript):
    name = "getitem"
    traits = frozenset({Pure()})
    obj: SSAValue = info.argument(print=False)
    index: SSAValue = info.argument(print=False)
    result: ResultValue = info.result(types.Any)


@statement(dialect=dialect)
class SetItem(Subscript):
    name = "setitem"
    obj: SSAValue = info.argument(print=False)
    value: SSAValue = info.argument(print=False)
    index: SSAValue = info.argument(print=False)
