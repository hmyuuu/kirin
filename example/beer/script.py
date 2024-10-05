from dialect import dialect
from stmts import Drink, NewBeer, Pour, Puke

from interp import BeerInterpreter as BeerInterpreter
from kirin.ir import dialect_group
from kirin.prelude import basic_no_opt
from kirin.rewrite import Fixpoint, Walk
from rewrite import RandomWalkBranch


# create our own beer dialect, it runs a random walk on the branches
@dialect_group(basic_no_opt.add(dialect))
def beer(self):
    def run_pass(mt):
        Fixpoint(Walk(RandomWalkBranch())).rewrite(mt.code)

    return run_pass


# we are going to get drunk!
# add our beer dialect to the default dialect (builtin, cf, func, ...)


# type: ignore
@beer
def main(x):
    beer = NewBeer("budlight")  # type: ignore
    Drink(beer)  # type: ignore
    Pour(beer, 12)  # type: ignore
    Puke()
    if x > 1:
        Drink(NewBeer("heineken"))  # type: ignore
    else:
        Drink(NewBeer("tsingdao"))  # type: ignore
    return x + 1


main.code.print()
main(1)  # execute the function

# for i in range(10):
#     print("iteration", i)
#     main(i)  # now drink a random beer!
