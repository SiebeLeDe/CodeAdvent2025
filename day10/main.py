import pathlib as pl


def main():
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"


if __name__ == "__main__":
    main()
