# {{cookiecutter.project_name}}

## Dependencies

TODO: Add dependencies here that are not accounted for in the `pyproject.toml`.

* python3
* docker

## Installation

TODO: Add installation instructions here.

## Quick Start

Use the provided docker container to run the commands.

1. build the container

```
./scripts/build-container.sh
```

2. use the container

```
./scripts/run-command.sh    
```

These commands delegate to `nox`.

3. explore the container

```
./scripts/launch-shell-in-container.sh
```

## Run Tests

```bash
./scripts/run-command.sh -rs tests
```

## Documentation

Source documentation is at:

* [Documentation Root](./docs/content/index.rst)

Or you can build the documentation:

TODO: Show docs help. 

```bash
./scripts/run-command.sh -rs docs
```

...and then launch a browser to view the documentation:

```
firefox docs/_build/html/index.html
```

## Details

TODO: add any further in-depth details here.