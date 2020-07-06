import csv
from decimal import Decimal

import click

NAN_VALUE = "nan"


# CSV UTILS
def read_csv(path):
    """
    Returns iterable csv object
    """
    with open(path, newline="\n") as csvfile:
        for row in csv.reader(csvfile, delimiter=","):
            yield row


# MATRIX COMPUTATIONS
def combine_seen(row, prev_row):
    """
    :param row: row for initial calculations
    :param prev_row: row requiring finished calculations
    :return: (completed prev_row, partial row)
    """
    prev_val = None
    backfill = False
    for index, current_val in enumerate(row):
        if current_val.strip() == NAN_VALUE:
            # Combine all the values we have access to
            count = 0
            total_value = 0
            # TODO: Handle a 'nan' prev val
            if prev_val:
                count += 1
                total_value += prev_val
            if prev_row:
                count += 1
                # Assume it will be a valid float
                total_value += Decimal(prev_row[index])
            row[index] = {"value": total_value, "count": count}
            backfill = True
        else:
            current_val = Decimal(current_val)
            prev_val = current_val
            if backfill:
                row[index - 1]["value"] += current_val
                row[index - 1]["count"] += 1
                backfill = False
        if prev_row and type(prev_row[index]) != str:
            # Add the final value to complete the previous row
            prev_row_val = prev_row[index]
            # TODO: Handle a 'nan' current val
            prev_row[index] = (prev_row_val["value"] + current_val) / (
                prev_row_val["count"] + 1
            )

    return prev_row, row


def compute(input_path):
    """
    :param input_path: path to file to be read

    Generator to produce complete row for writing
    """
    prev_row = None
    # TODO: Handle validation of row length
    for row in read_csv(input_path):
        complete_row, prev_row = combine_seen(row, prev_row)
        if complete_row:
            print(".", end="")
            yield complete_row
    # Compute final line
    print(".", end="")
    yield [
        current_val["value"] / current_val["count"]
        if type(current_val) != str
        else current_val
        for index, current_val in enumerate(prev_row)
    ]


# VALIDATORS
def validate_csv(ctx, param, value):
    """
    Ensure paths are csv files
    """
    if value and not value.endswith(".csv"):
        raise click.BadParameter("Input file must be in CSV format.")
    return value


def derive_output_path(value):
    """
    Inject "_out" into path
    """
    return value.rstrip(".csv") + "_out.csv"


def default_output(ctx, param, value):
    """
    Set a default output path if none is passed in
    """
    if value:
        return validate_csv(ctx, param, value)
    else:
        return derive_output_path(ctx.params.get("input_path"))


def command(input_path, output_path):
    """
    Extract logic from the click decorated main
    """
    print(f"INPUT PATH PROVIDED: {input_path}")
    with open(output_path, "w") as output_file:
        writes = csv.writer(output_file, delimiter=",")
        writes.writerows(compute(input_path))
    print(f"\n OUTPUT WRITTEN TO: {output_path}")


# MAIN COMMAND
@click.command()
@click.option(
    "-I",
    "--input_path",
    required=True,
    callback=validate_csv,
    help="Input file path. Input file must be CSV.",
    type=click.Path(),
)
@click.option(
    "-O",
    "--output_path",
    default=None,
    callback=default_output,
    help="Output file path. Output file must be CSV.",
    type=click.Path(),
)
def main(input_path, output_path):
    command(input_path, output_path)


if __name__ == "__main__":
    main()

"""
TODO: Interpolate neighbouring NAN's

store uncalculated value coordinate in a tuple as dict key
i.e. (1, 2) : {value: 1, count: 2}

If a calculation allows us to solve any others, fill that in and repeat.
Ultimately looking for count of 3, unless edge square, in which case - 1
for each edge
"""
