import pathlib as pl
from dataclasses import dataclass


@dataclass
class JunctionBox:
    x: int
    y: int
    z: int

    def __str__(self) -> str:
        return f"{self.x},{self.y},{self.z}"


def read_junction_boxes_file(file_path: pl.Path) -> list[JunctionBox]:
    """
    Reads a file containing the positions of junction boxes in a grid.
    Each line represents one junction box with x,y,z coordinates separated by commas.

    162,817,812
    57,618,57
    906,360,560
    592,479,940
    352,342,300
    466,668,158
    """
    lines = file_path.read_text().splitlines()
    junction_boxes = []
    for line in lines:
        x, y, z = map(int, line.strip().split(","))
        junction_boxes.append(JunctionBox(x, y, z))
    return junction_boxes


def calculate_straight_line_distance(box1: JunctionBox, box2: JunctionBox) -> float:
    """
    Calculates the straight-line (Euclidean) distance between two junction boxes.
    """
    return ((box1.x - box2.x) ** 2 + (box1.y - box2.y) ** 2 + (box1.z - box2.z) ** 2) ** 0.5


def calcate_distances_between_junction_boxes(junction_boxes: list[JunctionBox]) -> dict[tuple[int, int], float]:
    """
    Calculates the straight-line distances between all pairs of junction boxes.

    Returns a dictionary with keys as tuples of junction box indices and values as the distances.
    """
    distances = {}
    for i, box1 in enumerate(junction_boxes):
        for j, box2 in enumerate(junction_boxes[i + 1 :], start=i + 1):
            distances[i, j] = calculate_straight_line_distance(box1, box2)

    return dict(sorted(distances.items(), key=lambda item: item[1]))


def create_circuits(junction_boxes: list[JunctionBox], sorted_distances: dict[tuple[int, int], float], max_iterations: int) -> list[set[int]]:
    """
    Connects junction boxes based on the sorted distances to form circuits.

    Returns a list of sets, where each set contains the indices of junction boxes in a circuit.
    """
    circuits: list[set[int]] = [set([i]) for i in range(len(junction_boxes))]

    iteration = 0
    for (i, j), dist in sorted_distances.items():
        iteration += 1
        # Find the circuits that contain box i and box j
        circuit_i = next(c for c in circuits if i in c)
        circuit_j = next(c for c in circuits if j in c)

        if circuit_i != circuit_j:
            # Merge the two circuits
            circuit_i.update(circuit_j)
            circuits.remove(circuit_j)
            print(f"Connecting box {junction_boxes[i]} and box {junction_boxes[j]} with distance {dist:.2f}.")

        if iteration >= max_iterations:
            break  # Limit iterations for example

        if len(circuits) == 1:
            print("All junction boxes are now connected into a single circuit.")
            print(f"Last connection made between box {junction_boxes[i]} and box {junction_boxes[j]} with distance {dist:.2f} and coordinate multiplication {junction_boxes[i].x * junction_boxes[j].x}")
            break

    circuits.sort(key=lambda c: len(c), reverse=True)
    return circuits


def main():
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"

    junction_boxes = read_junction_boxes_file(input_file)

    # Sort on distance
    sorted_distances = calcate_distances_between_junction_boxes(junction_boxes)

    # Connect the closest boxes first by forming circuits.
    max_iterations = 10 if "example" in str(input_file) else 100_000
    circuits: list[set[int]] = create_circuits(junction_boxes, sorted_distances, max_iterations=max_iterations)
    print(f"\nFinal circuits formed: {circuits}") if len(circuits) < 10 else print(f"\nNumber of circuits formed: {len(circuits)}")

    if len(circuits) >= 3:
        print(f"Multiplication of the sizes of the three largest circuits: {circuits[:3]} -> {len(circuits[0]) * len(circuits[1]) * len(circuits[2])}")


if __name__ == "__main__":
    main()
