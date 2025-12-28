import pathlib as pl


def read_id_file(file_path: str | pl.Path) -> tuple[list[tuple[int, int]], list[int]]:
    """
    Reads the file containing (false) IDs and returns a tuple of lists:
        - List of tuples with ranges (start, end)
        - List of individual IDs

    The first part of the being consists of ranges in the format "start-end",
    and the second part consists of individual IDs, one per line.
    """
    ranges: list[tuple[int, int]] = []
    individual_ids: list[int] = []

    with open(file_path, "r") as file:
        lines = file.readlines()

        # Process ranges
        for line in lines:
            line = line.strip()
            if "-" in line:
                start, end = map(int, line.split("-"))
                ranges.append((start, end))
            elif line.isdigit():
                individual_ids.append(int(line))

    return ranges, individual_ids


def determine_fresh_and_spoiled_ids(ranges: list[tuple[int, int]], individual_ids: list[int]) -> tuple[list[int], list[int]]:
    """
    Determines which individual IDs belong to fresh and spoiled food items based on the provided ranges.
    Fresh food IDs fall within any of the speicified ranges, while spoiled food IDs do not.
    """
    fresh_ids: list[int] = []
    spoiled_ids: list[int] = []

    for id_ in individual_ids:
        is_fresh = any(start <= id_ <= end for start, end in ranges)
        if is_fresh:
            fresh_ids.append(id_)
        else:
            spoiled_ids.append(id_)

    return fresh_ids, spoiled_ids


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merges overlapping and contiguous ranges into a list of non-overlapping ranges."""
    if not ranges:
        return []

    # Sort ranges by their start values to make the merging process more efficient
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    merged_ranges = [sorted_ranges[0]]

    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged_ranges[-1]

        if current_start <= last_end + 1:  # Overlapping or contiguous ranges
            merged_ranges[-1] = (last_start, max(last_end, current_end))
        else:
            merged_ranges.append((current_start, current_end))

    return merged_ranges


def determine_number_of_fresh_ids_from_ranges(ranges: list[tuple[int, int]]) -> int:
    """From a list of sorted, non-overlapping ranges, determine the total number of unique fresh IDs, which are IDs that fall within any of the specified ranges."""
    total_fresh_ids = 0

    for start, end in ranges:
        total_fresh_ids += end - start + 1

    return total_fresh_ids


def main():
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"

    ranges, ids = read_id_file(input_file)

    merged_ranges = merge_ranges(ranges)
    print(f"Merged Ranges: {merged_ranges}")
    print(f"Size reduced from {len(ranges)} to {len(merged_ranges)} ranges after merging.")

    fresh_ids, spoiled_ids = determine_fresh_and_spoiled_ids(merged_ranges, ids)
    # print(f"Fresh IDs: {fresh_ids}")
    # print(f"Spoiled IDs: {spoiled_ids}")

    n_fresh_ids = len(fresh_ids)
    n_spoiled_ids = len(spoiled_ids)
    print(f"Number of Fresh IDs: {n_fresh_ids}")
    print(f"Number of Spoiled IDs: {n_spoiled_ids}")

    total_fresh_ids = determine_number_of_fresh_ids_from_ranges(merged_ranges)
    print(f"Total number of unique Fresh IDs from ranges: {total_fresh_ids}")


if __name__ == "__main__":
    main()
