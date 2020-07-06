# Interpolation CLI

This CLI is designed to take a csv file containing multiple, equal length rows where each cell contains either a float, or the value 'nan'.

It will average non-diagonal neighbours (above, below, left and right) to interpolate a value for that cell.

## Usage

```
interpolate -I <path_to_file> -O <path_to_output>
```

#### Arguments

- `-I`, `--input_path`: path to chosen input file
- `-O`, `--output_path`: path to write output
- `--help`: show help

#### Example Input

```
[
["37.454012", "95.071431", "73.199394", "59.865848", "nan"],
["15.599452", "5.808361", "86.617615", "60.111501", "70.807258"],
["2.058449", "96.990985", "nan", "21.233911", "18.182497"],
["nan", "30.424224", "52.475643", "43.194502", "29.122914"],
["61.185289", "13.949386", "29.214465", "nan", "45.606998"],
]
```

#### Example Output

```
[
["37.454012", "95.071431", "73.199394", "59.865848", "65.336553"],
["15.599452", "5.808361", "86.617615", "60.111501", "70.807258"],
["2.058449", "96.990985", "64.3295385", "21.233911", "18.182497"],
["31.222654", "30.424224", "52.475643", "43.194502", "29.122914"],
["61.185289", "13.949386", "29.214465", "39.338655", "45.606998"],
]
```

## Installation

### PipX (Recommended)

If you use [pipx](https://pipxproject.github.io/pipx/) to handle global installs, you can install this package as the `interpolate` command.

First, install poetry and pipx. Then install dependencies via poetry (see below).

```
poetry build # creates the wheel for pipx to install
pipx install dist/interpolate-0.1.0-py3-none-any.whl

# Usage:
interpolate -I <path_to_input>
```

### Virtual Env

Package management is handled by [Poetry](https://python-poetry.org/docs/).

With poetry installed, you should be able to get started with a simple:

```
poetry install --no-root

# or without dev dependencies

poetry install --no-root --no-dev
```

You can then run the command via:

```
poetry run interpolate -I <path_to_input>

i.e.
poetry run interpolate -I ./example_data/input_test_data.csv
```

### Docker

A Dockerfile is provided for convenience and reproducibility. The image can be built and run as:

```
docker build -t interpolate .

docker run --rm -v $PWD/example_data:/app/example_data interpolate -I example_data/input_test_data.csv
```

Note: Input and output directories need to be mounted using `-v`.

## Development

### Tests

Tests are written using [pytest](https://docs.pytest.org/en/latest/contents.html).

To run tests, after installing dependencies:

```
pytest
```
