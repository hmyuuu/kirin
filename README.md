# KIRIN

[![CI](https://github.com/QuEraComputing/kirin/actions/workflows/ci.yml/badge.svg)](https://github.com/QuEraComputing/kirin/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/QuEraComputing/kirin/graph/badge.svg?token=lkUZ9DTqy4)](https://codecov.io/gh/QuEraComputing/kirin)

*K*ernel *I*ntermediate *R*epresentation *IN*frastructure

_The multi-level intermediate representation (MLIR) compiler for high-level semantics in Python._

> [!IMPORTANT]
>
> This project is in the early stage of development. API and features are subject to change.

## Installation

### Install via `rye` (Recommended)

This package is registered in `quera-algo` repository. If you have not set up the repository, you can add the following to `~/.rye/config.toml`:

```toml
[[sources]]
name = "quera-algo"
url = "https://rluo@quera.com:<PASSWORD>@quera.jfrog.io/artifactory/api/pypi/quera-algo/simple"
type = "index"
```

where `<PASSWORD>` can be found on QuEra's JFrog Artifactory. Then you can install the package by:

```bash
rye add kirin-toolchain
rye sync
```

### Install via `pip` (Less Recommended)

Or you can use it via `pip` by copying the following to `~/.pip/pip.conf`:

```conf
[global]
index-url = https://rluo@quera.com:<PASSWORD>@quera.jfrog.io/artifactory/api/pypi/quera-algo/simple
```

then install the package by:

```bash
pip install kirin-toolchain
```

## See Also

Several dialects are defined in their own packages. The close relatives are
defined as namespace packages. See [kirin-workspace](https://github.com/QuEraComputing/kirin-workspace) to develop them together.

## Roadmap

Some features of this compiler before we all in [MLIR][mlir]:

- [x] a [MLIR-like][mlir] IR infrastructure specialized for FLAIR
  - [ ] progressive lowering
  - [x] dialects for several compilation stages
- [x] a [Julia-like][julia] JIT compiler
  - [x] abstract interpretation
  - [x] linear type system on SSA with type inference
- [x] [Jax][jax]-like frontend

## References

- current [flair.py][flair.py]
- [xdsl][xdsl]
- [mlir][mlir]
- [Julia/base/compiler][julia] compiler
- [jax][jax]

[flair.py]: https://github.com/QuEraComputing/flair.py
[xdsl]: https://github.com/xdslproject/xdsl
[mlir]: https://mlir.llvm.org/
[julia]: https://github.com/JuliaLang/julia/tree/master/base/compiler
[jax]: https://jax.readthedocs.io/en/latest/
