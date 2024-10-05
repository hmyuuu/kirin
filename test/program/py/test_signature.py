from kirin.dialects.py import types
from kirin.prelude import basic


@basic
def complicated_type(x: list[tuple[float, float, list[float]]]):
    return x


def test_complicated_type():
    typ = complicated_type.arg_types[0]
    assert isinstance(typ, types.PyGeneric)
    assert typ.is_subseteq(
        types.List[types.Tuple[types.Float, types.Float, types.List[types.Float]]]
    )
