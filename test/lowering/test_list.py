from kirin.dialects import cf, func
from kirin.dialects.py import data, stmts, types
from kirin.lowering import Lowering
from kirin.prelude import basic

lowering = Lowering([cf, func, data, types, stmts])


def test_empty_list():

    def empty_list():
        x = []
        return x

    code = lowering.run(empty_list)

    list_stmt = code.body.blocks[0].stmts.at(0)  # type: ignore

    assert isinstance(list_stmt, stmts.NewList)
    assert len(list_stmt._results) == 1

    res = list_stmt._results[0]
    assert res.type.is_subseteq(types.List)


def test_list_append():

    @basic
    def test_append():
        x = []
        stmts.Append(x, 1)
        stmts.Append(x, 2)
        return x

    y = test_append()

    assert len(y) == 2
    assert y[0] == 1
    assert y[1] == 2


def test_recursive_append():

    @basic
    def for_loop_append(cntr: int, x: list, n_range: int):
        if cntr < n_range:
            stmts.Append(x, cntr)
            for_loop_append(cntr + 1, x, n_range)

        return x

    y = for_loop_append(0, [], 10)

    assert len(y) == 10
    assert y == [i for i in range(10)]
