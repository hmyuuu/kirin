from random import randint

from attrs import Beer
from dialect import dialect
from stmts import Drink, NewBeer, Pour, Puke, RandomBranch

from kirin.interp import DialectInterpreter, Interpreter, ResultValue, Successor, impl


@dialect.register
class BeerInterpreter(DialectInterpreter):

    @impl(NewBeer)
    def new_beer(self, interp: Interpreter, stmt: NewBeer, values: tuple):
        return ResultValue(Beer(values[0]))

    @impl(Drink)
    def drink(self, interp: Interpreter, stmt: Drink, values: tuple):
        print(f"Drinking {values[0].brand}")
        return ResultValue()

    @impl(Pour)
    def pour(self, interp: Interpreter, stmt: Pour, values: tuple):
        print(f"Pouring {values[0].brand} {values[1]}")
        return ResultValue()

    @impl(Puke)
    def puke(self, interp: Interpreter, stmt: Puke, values: tuple):
        print("Puking!!!")
        return ResultValue()

    @impl(RandomBranch)
    def random_branch(self, interp: Interpreter, stmt: RandomBranch, values: tuple):
        frame = interp.state.current_frame()
        if randint(0, 1):
            return Successor(
                stmt.then_successor, *frame.get_values(stmt.then_arguments)
            )
        else:
            return Successor(
                stmt.else_successor, *frame.get_values(stmt.then_arguments)
            )
