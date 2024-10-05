from kirin.interp import Interpreter
from kirin.prelude import basic_no_opt
from kirin.rewrite import Walk
from kirin.rules.inline import Inline


@basic_no_opt
def somefunc(x: int):
    return x - 1


@basic_no_opt
def main(x: int):
    return somefunc(x) + 1


def test_simple():
    inline = Inline(heuristic=lambda x: True, interp=Interpreter(main.dialects))
    a = main(1)
    main.code.print()
    Walk(inline).rewrite(main.code)
    main.code.print()
    b = main(1)
    assert a == b
