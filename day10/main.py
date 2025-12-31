import pathlib as pl
import numpy as np
from dataclasses import dataclass
from numpy.typing import NDArray
import tabulate


@dataclass
class Schematic:
    lights: NDArray[np.int_]  # One-dimensional array representing light states of size (n_lights,)
    button_wiring: NDArray[np.int_]  # Two-dimensional array of size (n_lights, n_buttons)
    joltage_requirements: NDArray[np.int_]

    @property
    def matrix_representation(self) -> NDArray:
        """
        Returns a matrix representation of the schematic combining lights and button wiring.
        The first row represents the light states, and the subsequent rows represent button wiring.
        """
        n_lights, n_buttons = self.button_wiring.shape
        matrix = np.zeros((n_lights, n_buttons + 1), dtype=int)
        matrix[:, 0] = self.lights
        matrix[:, 1:] = self.button_wiring
        return matrix

    def __str__(self):
        header = ["Light State"] + [f"Button {i}" for i in range(self.button_wiring.shape[1])]
        table = tabulate.tabulate(self.matrix_representation, headers=header, tablefmt="simple")
        joltage_str = f"Joltage Requirements: {self.joltage_requirements.tolist()}"
        return f"{table}\n{joltage_str}"


def read_initialization_procedure_file(file_path: pl.Path) -> list[Schematic]:
    """
    Reads in the initialization procedure file and returns the schematics in array format.

    Format:
    [light diagram] (button wiring schematics) {joltage requirements}
    [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

    with "." representing off lights and "#" representing on lights, and counting from the 0 index.

    """
    content = file_path.read_text().strip().splitlines()
    schematics = []

    for line in content:
        lights, *wiring, joltage = line.split(" ")
        lights_array = np.array([1 if char == "#" else 0 for char in lights[1:-1]], dtype=int)

        n_lights = lights_array.shape[0]
        n_buttons = len(wiring)
        wiring_array = np.zeros((n_lights, n_buttons), dtype=int)
        for button_idx, wire in enumerate(wiring):
            if "," in wire:
                connected_lights = wire[1:-1].split(",")
            else:
                connected_lights = [wire[1:-1]]

            for light in connected_lights:
                light_idx = int(light)
                wiring_array[light_idx, button_idx] = 1
        joltage_array = np.array([jolt for jolt in joltage[1:-1].split(",")], dtype=int)
        schematic = Schematic(lights=lights_array, button_wiring=wiring_array, joltage_requirements=joltage_array)
        schematics.append(schematic)
    return schematics


def solve_gf2(matrix: NDArray[np.int_], target: NDArray[np.int_]) -> tuple[int, NDArray[np.int_], NDArray[np.int_]]:
    """Solve the system using Gaussian elimination over GF(2)"""
    num_rows, num_cols = matrix.shape
    for col in range(num_cols):
        # Find a row with a 1 in this column
        for row in range(col, num_rows):
            if matrix[row, col] == 1:
                break
        else:
            continue
        # Swap rows
        matrix[[col, row]] = matrix[[row, col]]
        target[[col, row]] = target[[row, col]]
        # Eliminate other rows
        for row in range(num_rows):
            if row != col and matrix[row, col] == 1:
                matrix[row] ^= matrix[col]
                target[row] ^= target[col]
    # Count the minimum number of presses
    return sum(target), matrix, target


def main():
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"

    schematics = read_initialization_procedure_file(example_file)
    [print(schematic) for schematic in schematics]

    total_presses = 0
    for schematic in schematics:
        matrix = schematic.button_wiring.copy()
        target = schematic.lights.copy()
        min_presses, final_matrix, target = solve_gf2(matrix[:, 1:], target)
        total_presses += min_presses
        print(f"Minimum button presses needed: {min_presses}")
        print(f"Final button states: {target.tolist()}")
        print(final_matrix)

    print(f"Total minimum button presses for all schematics: {total_presses}")


if __name__ == "__main__":
    main()
