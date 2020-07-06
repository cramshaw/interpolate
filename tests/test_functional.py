from interpolate.interpolate import command

EXAMPLE_PATH = "./examples/input_test_data.csv"
EXAMPLE_COMPLETE_PATH = "./examples/interpolated_test_data.csv"


def test_main(tmpdir):
    output_path = tmpdir.join("output.csv")
    command(EXAMPLE_PATH, output_path)
    with open(output_path, "r") as outfile:
        with open(EXAMPLE_COMPLETE_PATH, "r") as complete_file:
            assert outfile.read() == complete_file.read()
