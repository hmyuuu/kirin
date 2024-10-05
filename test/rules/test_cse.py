from kirin.prelude import basic_no_opt
from kirin.rewrite import Fixpoint, Walk
from kirin.rules.cse import CommonSubexpressionElimination


@basic_no_opt
def badprogram(x: int, y: int) -> int:
    a = x + y
    b = x + y
    x = a + b
    y = a + b
    return x + y


def test_cse():
    before = badprogram(1, 2)
    cse = CommonSubexpressionElimination()
    Fixpoint(Walk(cse)).rewrite(badprogram.code)
    after = badprogram(1, 2)

    assert before == after
