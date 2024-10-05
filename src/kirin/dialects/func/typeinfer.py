from kirin.analysis.dataflow.typeinfer import TypeInference
from kirin.dialects.func.dialect import dialect
from kirin.dialects.func.interp import Interpreter
from kirin.dialects.func.stmts import Return
from kirin.dialects.py import types
from kirin.interp import ReturnValue, impl


# NOTE: a lot of the type infer rules are same as the builtin dialect
@dialect.register(key="typeinfer")
class TypeInfer(Interpreter):
    @impl(Return)
    def return_(
        self, interp: TypeInference, stmt: Return, values: tuple
    ) -> ReturnValue:
        if not values:
            return ReturnValue(types.NoneType)
        else:
            return ReturnValue(*values)
