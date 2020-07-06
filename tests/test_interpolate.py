from decimal import Decimal

import pytest
from click import BadParameter

from interpolate.interpolate import (
    combine_seen,
    compute,
    derive_output_path,
    read_csv,
    validate_csv,
)

EXAMPLE_PATH = "./example_data/input_test_data.csv"
INPUT = [
    ["37.454012", "95.071431", "73.199394", "59.865848", "nan"],
    ["15.599452", "5.808361", "86.617615", "60.111501", "70.807258"],
    ["2.058449", "96.990985", "nan", "21.233911", "18.182497"],
    ["nan", "30.424224", "52.475643", "43.194502", "29.122914"],
    ["61.185289", "13.949386", "29.214465", "nan", "45.606998"],
]
PARTIAL = [
    [
        "37.454012",
        "95.071431",
        "73.199394",
        "59.865848",
        {"count": 1, "value": Decimal("59.865848")},
    ],
    ["15.599452", "5.808361", "86.617615", "60.111501", "70.807258"],
    [
        "2.058449",
        "96.990985",
        {"value": Decimal("204.842511"), "count": 3},
        "21.233911",
        "18.182497",
    ],
    [
        {"count": 2, "value": Decimal("32.482673")},
        "30.424224",
        "52.475643",
        "43.194502",
        "29.122914",
    ],
]

OUTPUT = [
    ["37.454012", "95.071431", "73.199394", "59.865848", Decimal("65.336553")],
    ["15.599452", "5.808361", "86.617615", "60.111501", "70.807258"],
    ["2.058449", "96.990985", Decimal("64.3295385"), "21.233911", "18.182497"],
    [Decimal("31.222654"), "30.424224", "52.475643", "43.194502", "29.122914"],
    ["61.185289", "13.949386", "29.214465", Decimal("39.338655"), "45.606998"],
]


def test_read_csv():
    """
    read_csv should return a generator of rows
    """
    rows = read_csv(EXAMPLE_PATH)
    assert next(rows) == INPUT[0]
    assert next(rows) == INPUT[1]


def test_combine_seen__no_previous():
    completed_row, row = combine_seen(INPUT[0], None)
    assert row == PARTIAL[0]
    assert completed_row is None


@pytest.mark.parametrize("partial,complete", [[1, 0], [2, 1], [3, 2]])
def test_combine_seen__partial(partial, complete):
    """
    Partial and completed rows are correctly returned
    """
    completed_row, row = combine_seen(INPUT[partial], PARTIAL[complete])
    assert completed_row == OUTPUT[complete]
    assert row == PARTIAL[partial]


def test_compute():
    """
    Functional transformation works
    """
    rows = list(compute(EXAMPLE_PATH))
    assert len(rows) == len(OUTPUT)
    for index, row in enumerate(rows):
        assert OUTPUT[index] == row


# CLI VALIDATORS


@pytest.mark.parametrize(
    "value,result", [["x.csv", True], ["x.cs", False], ["x.fastq", False]]
)
def test_validate_csv(value, result):
    if result:
        assert validate_csv("", "", value) == value
    else:
        with pytest.raises(BadParameter):
            validate_csv("", "", value)


@pytest.mark.parametrize(
    "value,result", [["x.csv", "x_out.csv"], ["a.b.csv", "a.b_out.csv"]]
)
def test_dervice_output_path(value, result):
    assert derive_output_path(value) == result
