from kirin.dialects.func.dialect import dialect
from kirin.dialects.func.stmts import Call, GetField, Lambda, Return
from kirin.exceptions import InterpreterError
from kirin.interp import DialectInterpreter, ResultValue, ReturnValue, concrete, impl
from kirin.ir import Method


@dialect.register
class Interpreter(DialectInterpreter):

    @impl(Call)
    def call(self, interp: concrete.Interpreter, stmt: Call, values: tuple):
        # NOTE: support kwargs after Call stmt stores the key names
        n_total = len(values)
        if stmt.kwargs.data:
            kwargs = dict(
                zip(stmt.kwargs.data, values[n_total - len(stmt.kwargs.data) :])
            )
        else:
            kwargs = None

        return interp.eval(
            values[0], values[1 : n_total - len(stmt.kwargs.data)], kwargs
        ).to_result()

    @impl(Return)
    def return_(self, interp: concrete.Interpreter, stmt: Return, values: tuple):
        if not values:
            return ReturnValue(None)
        elif len(values) == 1:
            return ReturnValue(values[0])
        else:
            raise InterpreterError(
                "multiple return values not supported, wrap in tuple"
            )

    @impl(GetField)
    def getfield(self, interp: concrete.Interpreter, stmt: GetField, values: tuple):
        mt: Method = values[0]
        return ResultValue(mt.fields[stmt.field])

    @impl(Lambda)
    def lambda_(self, interp: concrete.Interpreter, stmt: Lambda, values: tuple):
        return ResultValue(
            Method(
                mod=None,
                py_func=None,
                sym_name=stmt.name,
                arg_names=[
                    arg.name or str(idx)
                    for idx, arg in enumerate(stmt.body.blocks[0].args)
                ],
                dialects=interp.dialects,
                code=stmt,
                fields=values,
            )
        )
