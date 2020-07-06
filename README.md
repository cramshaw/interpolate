# Interpolation CLI

This CLI is designed to take a csv file containing multiple, equal length rows where each cell contains either a float, or the value 'nan'.

It will average non-diagonal neighbours (above, below, left and right) to interpolate a value for that cell.

## Usage

#### Arguments

- `-I`, `--input_path`: path to chosen input file
- `-O`, `--output_path`: path to write output
- `--help`: show help

## Installation

### Virtual Env

Package management is handled by [Poetry](https://python-poetry.org/docs/).

With poetry installed, you should be able to run for development with a simple

```
poetry install

# or without dev dependencies

poetry install --no-dev
```

You can then run the command via:

```
poetry run int -I <path_to_input>

i.e.
poetry run int -I ./examples/input_test_data.csv
```

### PipX

If you use [pipx](https://pipxproject.github.io/pipx/) to handle global installs, you can install this package as the `int` command.

First, add poetry, dependencies and pipx.

```
poetry build # creates the wheel for pipx to install
pipx install dist/interpolate-0.1.0-py3-none-any.whl

# Usage:
int -I <path_to_input>
```

### Docker

A Dockerfile is provided for convenience and reproducibility. The image can be built and run as:

```
docker build -t interpolate .

docker run --rm -v $PWD/examples:/app/examples interpolate -I examples/input_test_data.csv
```

Note: Input and output directories need to be mounted using `-v`.

## Development

### Tests

Tests are written using [pytest](https://docs.pytest.org/en/latest/contents.html).

To run tests, after installing dependencies:

```
pytest
```
