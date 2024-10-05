from dataclasses import dataclass

from kirin.dialects.func import Signature
from kirin.ir import (
    Block,
    CallableStmtInterface,
    HasSignature,
    SSAValue,
    Statement,
    TypeAttribute,
)
from kirin.rewrite import RewriteResult, RewriteRule


@dataclass
class ApplyType(RewriteRule):
    ret_type: TypeAttribute
    results: dict[SSAValue, TypeAttribute]

    def rewrite_Block(self, node: Block) -> RewriteResult:
        has_done_something = False
        for arg in node.args:
            if arg in self.results:
                arg.type = self.results[arg]
                has_done_something = True

        return RewriteResult(has_done_something=has_done_something)

    def rewrite_Statement(self, node: Statement) -> RewriteResult:
        if (fn_trait := node.get_trait(HasSignature)) and (
            call_trait := node.get_trait(CallableStmtInterface)
        ):
            signature = fn_trait.get_signature(node)
            body = call_trait.get_callable_region(node)
            inputs = [
                self.results[arg] if arg in self.results else signature.inputs[idx]
                for idx, arg in enumerate(body.blocks[0].args[1:])
            ]
            fn_trait.set_signature(node, Signature(tuple(inputs), self.ret_type))

        has_done_something = False
        for result in node._results:
            if result in self.results:
                result.type = self.results[result]
                has_done_something = True

        return RewriteResult(has_done_something=has_done_something)
