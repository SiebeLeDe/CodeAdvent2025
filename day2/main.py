import pathlib as pl


def read_ranges(file_path: pl.Path) -> list[tuple[int, int]]:
    """
    Reads a file containing pairs of ranges and returns them as a list of tuples
    It expects a comma-separated file in which each entry contains two ranges in the format "start-end"
    """
    file_lines = file_path.read_text().strip()
    ranges = []
    for entry in file_lines.split(","):
        begin, end, *_ = entry.split("-")
        ranges.append((int(begin), int(end)))
    return ranges


def determine_invalid_id(id: int, sequence_length: int) -> bool:
    """
    Determines if the given ID is invalid based on the specified sequence length.
    An ID is considered invalid if it consists of a sequence of digits repeated consecutively.

    Args:
        id (int): The ID to check.
        sequence_length (int): The length of the sequence to check for repetition.

    Returns:
        bool: True if the ID is invalid, False otherwise.
    """
    id_str = str(id)
    if len(id_str) % sequence_length != 0:
        return False

    sequence = id_str[:sequence_length]
    repeated_sequence = sequence * (len(id_str) // sequence_length)

    return repeated_sequence == id_str and not sequence.startswith("0")


def get_invalid_ids_from_range_first_part(range_pair: tuple[int, int]) -> set[int]:
    """
    Given a range defined by a tuple (start, end), returns how many and which IDs are invalid.

    An ID is considered invalid if:
    - any ID which is made only of some sequence of digits is repeated twice
    - sequences starting with "0" are ignored
    """
    start, end = range_pair
    invalid_ids = set()

    for id in range(start, end + 1):
        # Skip IDs with odd lengths
        if len(str(id)) % 2 != 0:
            continue

        if determine_invalid_id(id, len(str(id)) // 2):
            invalid_ids.add(id)

    return invalid_ids


def get_invalid_ids_from_range_second_part(range_pair: tuple[int, int]) -> set[int]:
    """
    Given a range defined by a tuple (start, end), returns how many and which IDs are invalid.
    In contrast to the first part, an invalid ID is now characterized by having any sequence of digits repeated, so at least twice in a consequential manner.

    An ID is considered invalid if:
    - any ID which is made only of some sequence of digits is repeated at least twice
    - sequences starting with "0" are ignored
    """
    start, end = range_pair
    invalid_ids = set()

    for id in range(start, end + 1):
        id_str = str(id)

        # Check for all possible sequence lengths
        for seq_length in range(1, len(id_str) // 2 + 1):
            if determine_invalid_id(id, seq_length):
                invalid_ids.add(id)
                break  # No need to check further sequence lengths

    return invalid_ids


def main():
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"

    ranges = read_ranges(input_file)

    total_invalid_ids = set()
    for range_pair in ranges:
        invalid_ids = get_invalid_ids_from_range_second_part(range_pair)
        print(f"Range {range_pair} has {len(invalid_ids)} invalid IDs: {sorted(invalid_ids)}")
        total_invalid_ids.update(invalid_ids)

    # Add up all invalid IDs from all ranges
    sum_of_invalid_ids = sum(total_invalid_ids)
    print(f"Total sum of all invalid IDs: {sum_of_invalid_ids}")


if __name__ == "__main__":
    main()
