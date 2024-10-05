from dataclasses import dataclass, field

from kirin.dialects import cf
from kirin.ir import Block, Pure, Statement
from kirin.rewrite import RewriteResult, RewriteRule


@dataclass(init=False)
class DeadCodeElimination(RewriteRule):
    # NOTE: replace this with a better algorithm
    # the complexity here is prob not suitable for a
    # large CFG
    cfg: dict[Block, set[Block]]
    _reverse_cfg: dict[Block, set[Block]] = field(repr=False)

    def __init__(self, cfg: dict[Block, set[Block]]):
        self.cfg = cfg
        self.update_cfg(cfg)

    def update_cfg(self, cfg: dict[Block, set[Block]]):
        self.cfg = cfg
        self._reverse_cfg = {}
        for node, successors in self.cfg.items():
            for succ in successors:
                self._reverse_cfg.setdefault(succ, set()).add(node)

    def rewrite_Block(self, node: Block) -> RewriteResult:
        if node in self.cfg:
            successors = self.cfg[node]
            if len(successors) > 1:
                return RewriteResult()

            # block has only one successor
            # if the terminator is cf.Branch
            # append its successor to this block
            # and remove the terminator, the new
            # terminator will be the successor's terminator
            if node.last_stmt and isinstance(node.last_stmt, cf.Branch):
                terminator = node.last_stmt
                successor = list(successors)[0]
                # not single edge in CFG
                if len(self._reverse_cfg[successor]) > 1:
                    return RewriteResult()

                stmt = successor.first_stmt
                while stmt is not None:
                    curr = stmt
                    stmt = stmt.next_stmt
                    curr.detach()
                    node.stmts.append(curr)
                terminator.delete()
                successor.delete()
        else:
            node.delete()
        return RewriteResult(has_done_something=True)

    def rewrite_Statement(self, node: Statement) -> RewriteResult:
        if not node.has_trait(Pure):
            return RewriteResult()

        for result in node._results:
            if result.uses:
                return RewriteResult()

        node.delete()
        return RewriteResult(has_done_something=True)
