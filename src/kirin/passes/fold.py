from dataclasses import dataclass

from kirin.analysis.dataflow.reachable import EmptyLattice, ReachableAnalysis
from kirin.interp import Interpreter
from kirin.ir import Method
from kirin.passes.abc import Pass
from kirin.rewrite import Chain, Fixpoint, Walk
from kirin.rules.dce import DeadCodeElimination
from kirin.rules.fold import ConstantFold


@dataclass
class Fold(Pass):

    def __post_init__(self):
        self.reachability = ReachableAnalysis(self.dialects)
        self.fold = Fixpoint(Walk(ConstantFold(Interpreter(self.dialects))))
        self.dce = DeadCodeElimination(cfg=self.reachability.worklist.visited)
        self.rule = Chain([Walk(self.fold), Walk(self.dce)])

    def __call__(self, mt: Method) -> None:
        self.reachability.eval(mt, tuple(EmptyLattice() for _ in mt.args))
        self.dce.update_cfg(self.reachability.worklist.visited)
        self.rule.rewrite(mt.code)
        self.reachability.worklist.visited.clear()  # clear CFG for next pass
