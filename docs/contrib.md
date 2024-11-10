# Contributing

Please see [Installation](install.md) for instructions on how to set up your development environment.

## Running the tests

We use `pytest` for testing. To run the tests, simply run:

```bash
pytest
```

or for a specific test file with the `-s` flag to show the output of the program:

```bash
pytest -s tests/test_program.py
```

lots of tests contains pretty printing of the IR themselves, so it's useful to see the output.

## Code style

We use `black` for code formatting. Besides the linter requirements, we also require the following
good-to-have practices:

### Naming

- try not to use abbreviation as names, unless it's a common abbreviation like `idx` for `index`
- try not create a lot of duplicated name prefix, e.g `ConstantInt` and `ConstantFloat`, instead use a new module to group them.
- try to use `snake_case` for naming variables and functions, and `CamelCase` for classes.

### Comments

- try not to write comments, unless it's really necessary. The code should be self-explanatory.
- if you have to write comments, try to use `NOTE:`, `TODO:` `FIXME:` tags to make it easier to search for them.

## Documentation

We use `just` for mangaging command line tools and scripts. It should be installed when you run `uv sync`. To build the documentation, simply run:

```bash
just doc
```

This will launch a local server to preview the documentation. You can also run `just doc-build` to build the documentation without launching the server.

## License

By contributing to this project, you agree to license your contributions under the Apache License 2.0 with LLVM Exceptions.
