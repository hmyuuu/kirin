## Kirin's Mission

By _Xiuzhe (Roger) Luo_, 2024-11-10

The field of scientific software has seen great development in the past decade. Scientists have been
building more and more sophisticated simulators (quantum circuit simulators, differential equation solvers,
differentiable solvers), and many different human controlable physical systems (neutral atoms, trapped ions,
superconducting qubits, optical lattices, etc) that may be used for multiple purposes.

These impressive progress urges the need for a more sophisticated way to interact with these simulators and physical systems. In software community, a domain-specific language (DSL) and a corresponding compiler is the way to go. However, building a DSL and a compiler is a non-trivial task, and it is not something that scientists are familiar with. This is why we are building Kirin.

## Why didn't use X?

This is a common question that one may ask when they see a new project. Here are some reasons why we are not using previous work.

### Why not use MLIR?

We have been trying to adopt MLIR since 2021, and we found that MLIR is a great project, but it is not easy to use for scientists. The scope of compilation problems that MLIR is trying to solve is too broad, and thus the complexity of the project is inevitably high. More specifically, we do not care about:

- low-level semantics
- traditional hardware targets
- high-quality native binary
- roundtrip-able IR text format

We do care about:

- high-level semantics
- new optimization techniques for the scientific problems
- interpretation and JIT compilation
- a frontend that is easy to use for scientists

In the quantum computing community, we have seen a lot of projects that are trying to build a quantum DSL and a compiler using MLIR. However, everyone will build their own dialects, Python frontend for the DSL, and another infrastructure to write IR passes in Python because how to compile such program is still under research. Big entities with sufficient bandwidth can afford to do this by hiring a lot of engineers, but for small companies and individual researchers, this is not feasible.

### Why not use xDSL?

Ok, after we have decided not to use MLIR, we were excited to see this project called [xDSL](https://github.com/xdslproject/xdsl) around 2023. We tried to play with it back in April 2024, and we found that the project is still sophisticated for scientists to use. Mostly because the project is built by professional compiler engineers and computer scientists and is also trying to replicate the MLIR infrastructure but in Python. The project is great, if you are interested in a friendlier version of MLIR in Python, you should definitely check it out. What was missing from our wishlist is:

- automated Python frontend
- different ways of interpretation (e.g abstract interpretation)
- Python type system instead of MLIR type attributes

maybe eventually this would be in xDSL but more realistically, because the focus is quite different and
xDSL was also new, the APIs are not stable yet and clearly have different priorities. We urgently need an infrastructure that we can build our own compilers on top of, so we seem to have no choice.

### Why not Julia compiler plugin?

For those who are familiar with my past work, I have been working with Julia since 2015. This is a great language
for scientific computing, and scientists with performance needs definitely love it. And in fact, the idea of
building some infrastructure to help scientists to build their own DSLs and compilers was initially from the
Julia community because of automatic differentiation and sparsity optimization (check the compiler plugin org).

## Choice of language & design

The choice of language here is Python. As most scientists are familiar with Python, and in QuEra Computing Inc,
we have a lot of Python-based software for hardware already. We do not want to add extra burden to the scientists
unless it is necessary. However, we are open to the idea of using other languages to improve certain components.

There are similar projects like [xDSL](https://github.com/xdslproject/xdsl) around at the beginning of Kirin around April 2024. We recommend you to check it out if you are interested in more sophisticated compiler infrastructure. However, after trying out the project, we found that the project is still sophisticated for scientists to use, and like most compiler toolchain, they don't really solve the problem that scientists care about: after defining the IR, rewrites, codegen, how would you actually program this DSL? This is why we are building Kirin in Python afterall.
