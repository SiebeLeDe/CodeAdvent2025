import pathlib as pl
import matplotlib.pyplot as plt
from itertools import combinations
from dataclasses import dataclass


@dataclass
class RedTile:
    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"


def read_red_tiles_file(file_path: pl.Path) -> list[RedTile]:
    """
    Reads a file containing the positions of red tiles on a grid.
    Each line represents one row of the grid, with coordinates separated by commas.

    Example file content:
    7,1
    11,1
    11,7
    9,7
    9,5
    2,5
    2,3
    7,3
    """
    lines = file_path.read_text().splitlines()
    red_tiles = [RedTile(x, y) for line in lines for x, y in [map(int, line.split(","))]]
    return red_tiles


def plot_red_tiles(red_tiles: list[RedTile]) -> None:
    """
    Plots the red tiles on a grid using matplotlib.
    """

    x_coords, y_coords = zip(*[(tile.x, tile.y) for tile in red_tiles])
    plt.scatter(x_coords, y_coords, color="red")
    plt.title("Red Tiles on Grid")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.grid(True)
    plt.xlim(0, max(x_coords) + 1)
    plt.ylim(0, max(y_coords) + 1)
    # invert the axes to match typical grid orientation
    plt.gca().invert_yaxis()

    plt.show()


def get_all_red_tile_combinations(red_tiles: list[RedTile]) -> list[tuple[RedTile, RedTile]]:
    """
    Generates all unique combinations of red tiles.
    Each combination is represented as a frozenset of tile coordinates.
    """
    return list(combinations(red_tiles, 2))


def calculate_area_of_red_tiles_opposite_corners(red_tiles: tuple[RedTile, RedTile]) -> int:
    """Given two opposite corners of a rectangle formed by red tiles, calculate the area which is the width (x) times height (y) difference."""

    # Apparently, we need to add 1 to include both edges
    width = 1 + abs(red_tiles[1].x - red_tiles[0].x)
    height = 1 + abs(red_tiles[1].y - red_tiles[0].y)

    if width == 0:
        width = 1
    if height == 0:
        height = 1
    return width * height


def main():
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"

    example_red_tiles = read_red_tiles_file(input_file)

    plot_red_tiles(example_red_tiles)

    all_combinations = get_all_red_tile_combinations(example_red_tiles)
    print("Total unique combinations of red tiles:", len(all_combinations))

    max_area = 0
    max_area_tiles = None
    for combo in all_combinations:
        area = calculate_area_of_red_tiles_opposite_corners(combo)
        if area > max_area:
            max_area = area
            max_area_tiles = combo

    print("Maximum area formed by red tiles:", max_area)
    print("Tiles forming maximum area:", max_area_tiles)


if __name__ == "__main__":
    main()
