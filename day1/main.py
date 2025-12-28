from enum import Enum
import pathlib as pl


class Direction(Enum):
    R = "R"
    L = "L"


def read_sequence(file_path: str | pl.Path) -> list[tuple[Direction, int]]:
    """
    Reads a sequence of directions and clicks in the format [R/L][integer] from a file.
    For example: R2, L3, R1, L4

    The sequence in the file is expected to be line-separated.
    """
    sequence = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                direction = Direction(line[0])
                clicks = int(line[1:])
                sequence.append((direction, clicks))
    return sequence


def turn_dial_by_step(step: tuple[Direction, int], total_rotations: dict[Direction, int], current_rotation: int) -> tuple[int, dict[Direction, int]]:
    """
    We consider a dial with numbers from 0 to 99 (100 numbers in total). Turning right (R) increases the number, turning left (L) decreases it.
    It time the dial reaches "0" from either direction, we count that as a full rotation. Also, we count all full rotations made during the turn, thus not only the ones that cross "0".
    Given a step (direction and number of clicks), the current rotation, and the total rotations made so far, this function returns the new rotation and updated total rotations.

    Args:
        step (tuple[Direction, int]): A tuple containing the direction (R or L) and the number of clicks.
        total_rotations (dict[Direction, int]): A dictionary tracking total rotations made in each direction.
        current_rotation (int): The current position of the dial (0-99).
    Returns:
        tuple[int, dict[Direction, int]]: The new rotation and updated total rotations.
    """
    direction, clicks = step

    if direction == Direction.R:
        total_rotations[Direction.R] += (clicks + current_rotation) // 100
        remaining_clicks = clicks % 100
        current_rotation = (current_rotation + remaining_clicks) % 100

    else:  # direction == Direction.L
        if current_rotation == 0:
            current_rotation = 100

        total_rotations[Direction.L] += abs((current_rotation - clicks) // 100)
        remaining_clicks = clicks % 100
        current_rotation = (current_rotation - remaining_clicks) % 100

        if current_rotation == 0:
            total_rotations[Direction.L] += 1
    return current_rotation, total_rotations


def main():
    parent_dir = pl.Path(__file__).parent
    test_sequence = read_sequence(parent_dir / "test_sequence.txt")
    main_sequence = read_sequence(parent_dir / "main_sequence.txt")

    current_rotation = 50
    total_rotations = {Direction.R: 0, Direction.L: 0}
    for i, step in enumerate(test_sequence, 1):
        new_rotation, total_rotations = turn_dial_by_step(step, total_rotations, current_rotation)
        print(f"Iteration {i}: {current_rotation} -> {new_rotation} by {step[0].value}{step[1]}, Total Rotations = {total_rotations[Direction.R] + total_rotations[Direction.L]}")
        current_rotation = new_rotation
    print(f"Final Rotation: {current_rotation}, Total Rotations: {total_rotations} = {total_rotations[Direction.R] + total_rotations[Direction.L]} in total")


1145

if __name__ == "__main__":
    main()
