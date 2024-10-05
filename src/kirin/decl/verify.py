import inspect

from beartype.door import is_subhint

from kirin import ir

from .base import BaseModifier
from .info import ArgumentField, Field, ResultField


class Verify(BaseModifier):

    def verify_mro(self):
        if not issubclass(self.cls, ir.Statement):
            raise TypeError(
                f"expected {self.cls.__name__} to be a subclass of ir.Statement"
            )

    def verify_fields(self):
        # Do we have any Field members that don't also have annotations?
        cls_annotations = inspect.get_annotations(self.cls)
        for name, value in self.cls.__dict__.items():
            if isinstance(value, Field) and name not in cls_annotations:
                raise TypeError(f"{name!r} is a field but has no type annotation")

        for f in self.fields:
            if isinstance(f, ArgumentField):
                if not (
                    is_subhint(f.annotation, ir.SSAValue)
                    or is_subhint(f.annotation, tuple[ir.SSAValue, ...])
                ):
                    raise TypeError(
                        f"{f.name!r} is an argument field but has an invalid type annotation"
                    )

                if is_subhint(f.annotation, ir.ResultValue):
                    raise TypeError(
                        f"{f.name!r} is an argument field but has an invalid type annotation {f.annotation}"
                    )

            if isinstance(f, ResultField) and not is_subhint(
                f.annotation, ir.ResultValue
            ):
                raise TypeError(
                    f"{f.name!r} is a result field but has an invalid type annotation"
                )
