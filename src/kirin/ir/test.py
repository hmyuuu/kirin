from kirin.ir import AnyType, SSAValue, TypeAttribute
from kirin.ir.derive import derive


@derive(id_hash=True)
class TestValue(SSAValue):

    def __init__(self, type: TypeAttribute | None = None) -> None:
        super().__init__()
        self.type = type or AnyType()

    @property
    def owner(self):
        raise NotImplementedError
