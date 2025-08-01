from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar
from dataclasses import dataclass

from kirin.ir.traits.abc import StmtTrait

if TYPE_CHECKING:
    from kirin.ir import Method, Region, Statement
    from kirin.dialects.func.attrs import Signature

StmtType = TypeVar("StmtType", bound="Statement")


@dataclass(frozen=True)
class CallableStmtInterface(StmtTrait, ABC, Generic[StmtType]):
    """A trait that indicates that a statement is a callable statement.

    A callable statement is a statement that can be called as a function.
    """

    @classmethod
    @abstractmethod
    def get_callable_region(cls, stmt: StmtType) -> "Region":
        """Returns the body of the callable region"""
        ...

    ValueType = TypeVar("ValueType")

    @classmethod
    @abstractmethod
    def align_input_args(
        cls, stmt: "StmtType", *args: ValueType, **kwargs: ValueType
    ) -> tuple[ValueType, ...]:
        """Permute the arguments and keyword arguments of the statement
        to match the execution order of the callable region input.
        """
        ...


@dataclass(frozen=True)
class HasSignature(StmtTrait, ABC):
    """A trait that indicates that a statement has a function signature
    attribute.
    """

    @classmethod
    def get_signature(cls, stmt: "Statement"):
        signature: Signature | None = stmt.attributes.get("signature")  # type: ignore
        if signature is None:
            raise ValueError(f"Statement {stmt.name} does not have a function type")

        return signature

    @classmethod
    def set_signature(cls, stmt: "Statement", signature: "Signature"):
        stmt.attributes["signature"] = signature

    def verify(self, node: "Statement"):
        from kirin.dialects.func.attrs import Signature

        signature = self.get_signature(node)
        if not isinstance(signature, Signature):
            raise ValueError(f"{signature} is not a Signature attribute")


class StaticCall(StmtTrait, ABC, Generic[StmtType]):

    @classmethod
    @abstractmethod
    def get_callee(cls, stmt: StmtType) -> "Method":
        """Returns the callee of the static call statement."""
        ...
