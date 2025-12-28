import pathlib as pl
import numpy as np


def read_battery_banks(file_path: pl.Path) -> list[int]:
    """
    Reads a file containing large numbers (batteries) separated by line breaks.
    """
    file_lines = file_path.read_text().strip().splitlines()
    return [int(line) for line in file_lines]


def determine_maximum_joltage_first_part(batteries: int) -> int:
    """
    Determines the maximum joltage from a given battery bank.
    The maximum joltage is defined by two batteries that can be turned on / selected.
    The indices of the two battiers must give the highest sum, but we cannot change the order of the batteries.

    For example, given the battery bank 234234234234278, the maximum joltage is 78 (the last two batteries).
    """
    first_battery = 0
    second_battery = 0

    for i, value in enumerate(str(batteries)):
        battery_value = int(value)

        if battery_value > first_battery and i != len(str(batteries)) - 1:
            second_battery = 1
            first_battery = battery_value
        elif battery_value > second_battery:
            second_battery = battery_value

    return int(f"{first_battery}{second_battery}")


def find_maximum_in_subsequence(batteries: str, start_index: int, end_index: int, min_value: int, max_value: int) -> tuple[int, int]:
    """
    Finds the maximum value in a subsequence of the battery string starting from start_index and having length length_sequence.
    The user may define the bounds (min_value and max_value) for the maximum search.

    Arguments:
        batteries (str): The string representation of the battery bank.
        start_index (int): The starting index of the subsequence.
        end_index (int): The ending index of the subsequence.
        min_value (int): The minimum value for the maximum search.
        max_value (int): The maximum value for the maximum search.
    Returns:
        tuple[int, int]: The maximum value found and its index within the subsequence.

    """
    subsequence = batteries[start_index:end_index]
    # print(f"Searching in subsequence: {subsequence} from index {start_index} to {end_index}.")
    maximum = 1
    maximum_index = 0
    for i, char in enumerate(subsequence):
        value = int(char)

        # Break if the value is the maximum possible
        if value == max_value:
            return value, i

        if min_value < value < max_value and value > maximum:
            maximum = value
            maximum_index = i

    return maximum, maximum_index


def determine_maximum_joltage_second_part(batteries: int, length_sequence: int) -> int:
    """
    Determines the maximum joltage from a given battery bank for a given sequence length.
    The maximum joltage is defined by n batteries (defined by length_sequence) that can be turned on / selected.
    The indices of the two battiers must give the highest sum, but we cannot change the order of the batteries.

    For example, given the battery bank 234234234234278 with length_sequence 2, the maximum joltage is 78 (the last two batteries).
    But, given the battery bank 234234234234278 with length_sequence 3, the maximum joltage is 478.
    """
    sequence = np.ones(length_sequence, dtype=int)
    sequence_indices = np.ones(length_sequence, dtype=int)

    str_batteries = str(batteries)
    start_index = 0
    for i in range(length_sequence):
        maximum, maximum_index = find_maximum_in_subsequence(str_batteries, start_index=start_index, end_index=(len(str_batteries) + 1) - (length_sequence - i), min_value=1, max_value=9)
        # print(f"Found maximum {maximum} at index {maximum_index} for position {i} in the sequence.")
        sequence[i] = maximum
        sequence_indices[i] = maximum_index
        start_index += maximum_index + 1

    sequence_str = [str(num) for num in sequence]

    return int("".join(sequence_str))


def main():
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"

    battery_banks = read_battery_banks(input_file)

    total_joltage = 0
    for battery_bank in battery_banks:
        max_joltage = determine_maximum_joltage_second_part(battery_bank, 12)
        print(f"Battery Bank: {battery_bank} => Maximum Joltage: {max_joltage}")
        total_joltage += max_joltage

    print(f"Total Maximum Joltage: {total_joltage}")


# 16923 is too low
# 17146 is too high

if __name__ == "__main__":
    main()
