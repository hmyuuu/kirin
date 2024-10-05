from dataclasses import dataclass

from kirin.dialects import cf
from kirin.dialects.py import stmts
from kirin.exceptions import InterpreterError
from kirin.interp import Interpreter
from kirin.ir import ConstantLike, Pure, ResultValue, Statement
from kirin.rewrite import RewriteResult, RewriteRule


@dataclass(init=False)
class ConstantFold(RewriteRule):
    interpreter: Interpreter

    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter

    def rewrite_Statement(self, node: Statement) -> RewriteResult:
        if isinstance(node, cf.ConditionalBranch):
            return self.rewrite_cf_ConditionalBranch(node)

        if not node.has_trait(Pure):
            return RewriteResult()

        if not all(
            isinstance(arg, ResultValue) and arg.stmt.has_trait(ConstantLike)
            for arg in node.args
        ):
            return RewriteResult()

        try:
            values = tuple(
                self.interpreter.run_stmt(arg.stmt, ()).values[0] for arg in node.args  # type: ignore
            )
            results: tuple = self.interpreter.run_stmt(node, values).values  # type: ignore
        except InterpreterError:
            return RewriteResult()

        new_stmts: list[stmts.Constant] = [stmts.Constant(result) for result in results]
        for old_result, stmt in zip(node._results, new_stmts):
            stmt.insert_before(node)
            old_result.replace_by(stmt.result)
            if old_result.name:
                stmt.result.name = old_result.name

        node.delete()
        return RewriteResult(has_done_something=True)

    def rewrite_cf_ConditionalBranch(self, node: cf.ConditionalBranch):  # noqa: F811
        if isinstance(node.cond, ResultValue) and node.cond.stmt.has_trait(
            ConstantLike
        ):
            try:
                value = self.interpreter.run_stmt(node.cond.stmt, ()).values[0]  # type: ignore
                if value:
                    cf.Branch(
                        arguments=node.then_arguments,
                        successor=node.then_successor,
                    ).insert_before(node)
                    node.delete()
                    return RewriteResult(has_done_something=True)
                else:
                    cf.Branch(
                        arguments=node.else_arguments,
                        successor=node.else_successor,
                    ).insert_before(node)
                    node.delete()
                    return RewriteResult(has_done_something=True)
            except InterpreterError:
                pass

        return RewriteResult()
