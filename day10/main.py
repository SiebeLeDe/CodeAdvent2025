import pathlib as pl
import numpy as np
from dataclasses import dataclass
from numpy.typing import NDArray
import tabulate
import json
from typing import Optional
import hashlib


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


def brute_force_solver(schematic: "Schematic") -> int:
    """
    Solves the button press problem using a brute-force approach. It generates all possible combinations of button presses and checks which one satisfies the light states and joltage requirements.

    This is not an efficient solution for large schematics but serves as a baseline for correctness.
    """
    n_buttons = schematic.button_wiring.shape[1]
    min_presses: int = 100000

    print("Number of buttons:", n_buttons, "Total combinations to check:", 1 << n_buttons)

    # Generate all possible combinations of button presses (2^n_buttons)
    # The i << n_buttons operation shifts the number 1 (0000000001 in binary, number of digits depends on precision) to the left by n_buttons places, effectively creating a binary number with n_buttons bits.
    # For example, if n_buttons is 3, then 1 << 3 would be 8 (00001000 in binary), which means we will check all combinations from 0 to 7 (00000000 to 00000111 in binary).
    for i in range(1 << n_buttons):
        presses = [int((i >> j) & 1) for j in range(n_buttons)]
        resulting_lights = np.zeros_like(schematic.lights)

        # Calculate the resulting light states based on the button presses
        # e.g., if the current button wiring is [[1, 0], [0, 1]] and the presses are [1, 0], the resulting lights would be [1, 0] (first button toggles the first light).
        # Pressing it again (presses [1, 1]) would toggle the first light again, resulting in [0, 0], which is given by the XOR operation.
        for button_idx, pressed in enumerate(presses):
            if pressed:
                resulting_lights ^= schematic.button_wiring[:, button_idx]

        # Check if the resulting light states match the target and joltage requirements
        if np.array_equal(resulting_lights, schematic.lights):
            min_presses = min(min_presses, sum(presses))

    return min_presses if min_presses != 100000 else -1  # Return -1 if no solution found


class ButtonPressSolver:
    """Context Class for solving the button press problem using a strategy pattern. It stores the results automatically (if used in a with statement) and can be extended to use different solving strategies."""

    def __init__(self, save_file: Optional[pl.Path] = None):
        self.save_file = save_file or (pl.Path(__file__).parent / "results.json")
        self.results = {}

    def solve(self, schematic: "Schematic") -> int:
        """Solves the button press problem for a given schematic and returns the minimum number of button presses needed."""
        schematic_hash = hashlib.md5(str(schematic).encode()).hexdigest()
        if schematic_hash in self.results:
            print("Result already computed, retrieving from saved results.")
            return self.results[schematic_hash]

        presses = brute_force_solver(schematic)
        self._save_result(schematic, presses)
        return presses

    def _save_result(self, schematic: "Schematic", presses: int):
        """Saves the result for a given schematic."""
        self.results[hashlib.md5(str(schematic).encode()).hexdigest()] = presses

    def __enter__(self):
        """Load the existing results from the save file if it exists, otherwise initialize an empty dictionary."""
        if self.save_file.exists():
            with self.save_file.open("r") as f:
                self.results = json.load(f)
        else:
            self.results = {}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            return False  # Don't suppress exceptions
        with self.save_file.open("w") as f:
            json.dump(self.results, f, indent=2)


def main():
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"
    save_file = current_dir / "results.json"

    schematics = read_initialization_procedure_file(input_file)

    total_presses = 0

    with ButtonPressSolver(save_file=save_file) as solver:
        for schematic in schematics:
            presses = solver.solve(schematic)
            print(f"Minimum button presses needed: {presses}")
            total_presses += presses


if __name__ == "__main__":
    main()
