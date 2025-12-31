import pathlib as pl
import matplotlib.pyplot as plt
from itertools import combinations
from dataclasses import dataclass

from typing import Sequence


@dataclass
class Tile:
    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"


def read_red_tiles_file(file_path: pl.Path) -> list[Tile]:
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
    red_tiles = [Tile(x, y) for line in lines for x, y in [map(int, line.split(","))]]
    return red_tiles


def add_green_tiles(red_tiles: list[Tile]) -> list[Tile]:
    """
    For part two, we add green tiles. Every red tile is connected to the red tile before and after it by a straight line of green tiles.
    The list also wraps, so the first and last red tiles are also connected by green tiles.
    """
    green_tiles = []
    num_red_tiles = len(red_tiles)

    for i in range(num_red_tiles):
        start_tile = red_tiles[i]
        end_tile = red_tiles[(i + 1) % num_red_tiles]  # Wrap around to the first tile

        if start_tile.x == end_tile.x:  # Vertical line
            y_range = range(min(start_tile.y, end_tile.y) + 1, max(start_tile.y, end_tile.y))
            for y in y_range:
                green_tiles.append(Tile(start_tile.x, y))
        elif start_tile.y == end_tile.y:  # Horizontal line
            x_range = range(min(start_tile.x, end_tile.x) + 1, max(start_tile.x, end_tile.x))
            for x in x_range:
                green_tiles.append(Tile(x, start_tile.y))
        else:
            raise ValueError("Tiles are not aligned either horizontally or vertically.")

    return red_tiles + green_tiles


def plot_tiles(red_tiles: Sequence[Tile], green_tiles: Sequence[Tile] | None = None, special_tiles: Sequence[Tile] | None = None) -> None:
    """
    Plots the red tiles on a grid using matplotlib.
    """
    x_coords, y_coords = zip(*[(tile.x, tile.y) for tile in red_tiles])
    plt.scatter(x_coords, y_coords, color="red")

    # if green_tiles:
    #     green_x, green_y = zip(*[(tile.x, tile.y) for tile in green_tiles])
    #     plt.scatter(green_x, green_y, color="green", alpha=0.5)

    if special_tiles:
        special_x, special_y = zip(*[(tile.x, tile.y) for tile in special_tiles])
        plt.scatter(special_x, special_y, color="blue", s=100, edgecolor="black")
        plt.fill([special_tiles[0].x, special_tiles[1].x, special_tiles[1].x, special_tiles[0].x], [special_tiles[0].y, special_tiles[0].y, special_tiles[1].y, special_tiles[1].y], color="blue", alpha=0.2)

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


def get_all_red_tile_combinations(red_tiles: list[Tile]) -> list[tuple[Tile, Tile]]:
    """
    Generates all unique combinations of red tiles.
    Each combination is represented as a frozenset of tile coordinates.
    """
    return list(combinations(red_tiles, 2))


def calculate_area_of_red_tiles_opposite_corners(red_tiles: tuple[Tile, Tile]) -> int:
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

    example_red_tiles = read_red_tiles_file(example_file)
    green_tiles = add_green_tiles(example_red_tiles)

    plot_tiles(example_red_tiles, green_tiles)

    all_combinations = get_all_red_tile_combinations(example_red_tiles)
    print("Total unique combinations of red tiles:", len(all_combinations))

    max_area = 0
    max_area_tiles = None
    for combo in all_combinations:
        area = calculate_area_of_red_tiles_opposite_corners(combo)
        if area > max_area:
            max_area = area
            max_area_tiles = combo

    plot_tiles(example_red_tiles, green_tiles, special_tiles=max_area_tiles)
    print("Maximum area formed by red tiles:", max_area)
    print("Tiles forming maximum area:", max_area_tiles)


if __name__ == "__main__":
    main()
