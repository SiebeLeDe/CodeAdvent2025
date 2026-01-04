import pathlib as pl
from dataclasses import dataclass


@dataclass
class Shape:
    index: int
    shape: list[str]
    area: int


@dataclass
class Diagram:
    width: int
    heigth: int
    shape_indices: list[int]


def read_file_with_shapes(file: pl.Path) -> tuple[list[Shape], list[Diagram]]:
    """
    Reads the file with shapes formatting into two parts:

    1. The items with their shapes
    2. The diagrams on which the shapes should fit

    Example shape:

    0:
    ###
    ##.
    ##.

    Example diagram:

    4x4: 0 0 0 0 2 0
    """
    content = file.read_text().splitlines()

    shapes = []
    number_of_items = [(line_index, int(line.split(":")[0])) for line_index, line in enumerate(content) if line.split(":")[0].isdigit()]
    for line_index, item_index in number_of_items:
        shape = content[line_index + 1 : line_index + 4]
        area = sum([1 for char in "".join(shape) if char == "#"])
        shapes.append(Shape(item_index, shape, area))

    diagrams = []
    diagram_line_indices = [line_index for line_index, line in enumerate(content) if "x" in line.split(":")[0]]
    for line_index in diagram_line_indices:
        dimensions, shape_indices = content[line_index].split(":")
        width, height = map(int, dimensions.split("x"))
        shapes_indices = [int(i) for i in shape_indices.split()]
        diagrams.append(Diagram(int(width), int(height), shape_indices=shapes_indices))

    return shapes, diagrams


def determine_valid_diagrams(shapes: list[Shape], diagrams: list[Diagram]) -> int:
    """Determines whether the shapes fit in a diagram by calculating the area of the diagram and summed/total area of the shapes belonging to a diagram"""

    valid_areas_count: int = 0
    for diagram in diagrams:
        area_diagram = diagram.heigth * diagram.width
        total_area_shapes = sum(shapes[shape_index].area * count_index for shape_index, count_index in enumerate(diagram.shape_indices))

        if total_area_shapes <= area_diagram:
            valid_areas_count += 1

    return valid_areas_count


def main():
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"

    shapes, diagrams = read_file_with_shapes(input_file)

    n_valid_diagrams = determine_valid_diagrams(shapes, diagrams)
    print(f"Number of valid diagrams: {n_valid_diagrams} of {len(diagrams)}")


if __name__ == "__main__":
    main()
