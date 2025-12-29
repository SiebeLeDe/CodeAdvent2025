import pathlib as pl


def read_in_manifold_file(file_path: pl.Path) -> list[str]:
    """
    Reads a file containing a "Tachyon manifold" diagram in which there is a Tachyon beam (initialized at S) propagating downwards.
    If the beam encounters a spliiter (represented by "^"), then the beam stops and it splits into two beams left and right of the splitter.
    Example diagram:

    .......S.......
    ...............
    .......^.......
    ...............
    ......^.^......
    ...............
    .....^.^.^.....
    ...............
    ....^.^...^....
    ...............
    ...^.^...^.^...
    ...............
    ..^...^.....^..
    ...............
    .^.^.^.^.^...^.
    ...............

    """
    lines = file_path.read_text().splitlines()
    manifold = [line.strip() for line in lines if line.strip()]
    return manifold


def initialize_beam_positions(manifold: list[str]) -> list[int]:
    """
    Finds the starting position(s) of the Tachyon beam(s) in the manifold diagram.

    Returns a list of integer indices representing the horizontal positions of the beams.
    """
    start_line = manifold[0]
    beam_positions = [i for i, char in enumerate(start_line) if char == "S"]
    return beam_positions


def propagate_beams(manifold_line: str, beam_positions: list[int]) -> tuple[str, int]:
    """
    Propagates the Tachyon beam(s) through the manifold diagram according to the splitting rules.
    Beams are represented by "|" characters in the diagram and we perform one step of propagation through the manifold.

    Arguments:
        - manifold_line: A string representing a single line of the Tachyon manifold diagram.
        - beam_positions: List of integer indices representing the current horizontal positions of the beams.

    Returns a tuple containing:
        - updated_manifold_line: A string representing the manifold line after propagation.
        - n_splitting_encounters: Integer count of how many times beams encountered splitters and split.
    """
    n_splitting_encounters = 0
    manifold_chars = list(manifold_line)

    for i, char in enumerate(manifold_chars):
        if i not in beam_positions:
            continue

        if char == "^":
            # Beam encounters a splitter, it splits into two beams left and right
            n_splitting_encounters += 1
            manifold_chars[i - 1] = "|"  # Beam stops at the splitter
            manifold_chars[i + 1] = "|"
        else:
            # Beam continues downwards
            manifold_chars[i] = "|"

    updated_manifold_line = "".join(manifold_chars)
    return updated_manifold_line, n_splitting_encounters


def propagate_quantum_beams(manifold_line: str, path_count_per_position: dict[int, int]) -> dict[int, int]:
    """
    Instead of propagating classical beams, we propagate quantum beams that can exist in superposition.
    For this, we need to keep track of all splitting events and update how many timelines are stacked on top of each other for each position.
    """
    for i, char in enumerate(manifold_line):
        if path_count_per_position.get(i, 0) == 0:
            continue

        if char == "^":
            # Beam encounters a splitter, it splits into two beams left and right
            n_paths = path_count_per_position[i]
            path_count_per_position[i - 1] = path_count_per_position.get(i - 1, 0) + n_paths
            path_count_per_position[i + 1] = path_count_per_position.get(i + 1, 0) + n_paths
            path_count_per_position[i] = 0  # Original beam is consumed at the splitter

    return path_count_per_position


def main():
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"

    manifold = read_in_manifold_file(example_file)

    new_manifold = manifold.copy()[:1]
    n_splitting_encounters = 0
    beam_positions = initialize_beam_positions(manifold)
    for line in manifold[1:]:  # Skip the first line since it only contains the starting beam(s)
        updated_line, n_splits = propagate_beams(line, beam_positions)
        new_manifold.append(updated_line)
        n_splitting_encounters += n_splits
        beam_positions = [i for i, char in enumerate(updated_line) if char == "|"]

    print("\nPart 1")
    print(f"Final beam positions in example: {beam_positions}")
    print(f"Number of splitting encounters in example: {n_splitting_encounters}")
    print("Final manifold diagram:")
    for line in new_manifold:
        print(line)


def main_part2():
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"

    manifold = read_in_manifold_file(input_file)
    path_count_per_position = {i: 1 for i in initialize_beam_positions(manifold)}
    print("\nPart 2")
    for i, line in enumerate(manifold[1:]):  # Skip the first line since it only contains the starting beam(s)
        print(f"{i}/{len(manifold) - 1} with {sum(path_count_per_position.values())} timelines")
        path_count_per_position = propagate_quantum_beams(line, path_count_per_position)
    print(f"Number of timelines (quantum): {sum(path_count_per_position.values())}")


if __name__ == "__main__":
    main()
    main_part2()
