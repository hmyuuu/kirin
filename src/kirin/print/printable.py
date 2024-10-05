from __future__ import annotations

import io
from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kirin.print import Printer


class Printable:

    def print(self, printer: Printer | None = None) -> None:
        """entry point of the printing process."""
        if printer is None:
            from kirin.print import Printer

            printer = Printer()
        self.print_impl(printer)
        printer.print_str("\n")  # add a new line in the end
        # printer.flush()

    def print_str(self, printer: Printer) -> str:
        stream = io.StringIO()
        printer = printer.similar(stream)
        self.print(printer)
        ret = stream.getvalue()
        stream.close()
        return ret

    @abstractmethod
    def print_impl(self, printer: Printer) -> None:
        raise NotImplementedError(f"print is not implemented for {type(self)}")
