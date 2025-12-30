from collections import deque
import matplotlib.pyplot as plt
import pathlib as pl
from typing import Sequence


# Copied from https://topaz.github.io/paste/#XQAAAQCSDAAAAAAAAAAzHIoib6pXbueH4X9F244lVRDcOZab5q1+VXn364pOX+NW/TQVpBRiYW/5lSDCrz/5aH0lPQUzjSRsCpGft6Hat7bHwZU1HVYdkliSBCxdRHbBWdUx5woQkwsnxQkVpufZuQC+eXYBVZF1Dv9f04YcjdrhW3O0p9ua2QKOqesWPBOgjPM9P87TKJnE2KFKNyKJYxDnhhJJzihoQ5Q2LqZDLc5X5TDvKTo89FJ7JEuEuR1NZRUx8YDX47+xuZOiKRltxI8Qez4qBOkw1xxJBIS0QEQQv+giIeyBgo64KRzdWBtFOXvJ66DSYFO4+ykmpeah3zEouMBAyPG3MqfR+xyNGBuN400/f3dGG0erBMLxOf2XFLEFfVxlef89SSD1kiO69ZRIbM58rwPxFKO45oEvmLzIrQ7YESrbNKbcKRQmtaOz2cPWODZuPzzLTmolFBgyHkHZ+f3etRAFJkMxASTUqFs6VrJHbH9ejSIqEqMzB31v4TxJH+NKu1I1rwD/+j7LJvhN/UVjLMMJa3oAMaxE5ID8MTKt4lnZUK7wJvGPCtfGTF0B0J1c/BlsKW1CBGhiMlAKW/i6pn3OtX+524H56uFt07Gg7Xw8aU/mIy523nTO3XLep0ykdSzUe6WGXTn6ITqGe/Npx52DD/G5XiRnFvFQvk/7LzaAqaRUiXWrmXFM0bteN+lD4j2gh66BMlHoyLRWUId8t4zu6r71NIgvGPlOKwjK6aE0w8FzmyoKbniUvOuQRGW8CbcN816DyKyA27rYkiXNFrePiCYP0sM2Ykhf6jnCisjMOfJV9vr0Dw1Hg8oKURYLjRsUZhZPlSbsGiqHtqJ+03M5hNLQRwTDtd5n2XUCJL7KOnnb3WHZqVyyQN4t9tk+dvC0pSB8nXoe1OQTTqXyXEXYPA7TibTymIAmQT2jVzY9mg1yINbGDYzKJ9d1mwNcfN5uBZ0kYnFdmWxNA7KrD3i3lwn/qxbl7ocFtLVtXGuEF65O/QE+RTxADUJQk8ZVROFXKTVLSaLrr8ZdJDOEdGNML91FpmsCvBA4QaXz7XFRoGJp6ESC2CW4BIkN553NQ0en+Ye3h+MNOOQ36R5tbn43RlHVQ55LD+aa0gU/GO8pSLuPifrYfe1NHzwLUcXu7Emx78i3bRmOBPt92Rd9dGeJBxyQGsryOLD/uGt7+vRY4ibcjtsUbtHp0N2ivcLaz4ZDIWtGxJFgUVsRSND9dlsa3n34Q82CYxxoaJs94uYkwzY788lMuF9cQ3mayS4FhAvD7tfEVrMNWj5iTON+JPdM9wd9lUMk8qyVZD+ON53Banrf6rRY5KWM4qLLd2fevL6DKT/ImdYvOLEiUAVITjhcvpa9QL7mjmL8LHCuCgUr92ufCctALjtyWYcT19HqDOm631bD7qfs9f72DjsIWOS/73NBkWb2ReqPY9yYFv6QYPgUeewNSxR8XgmDM8H5cChyR0NVZ76CjIWZmp95d4kCVVZMkYoFZv7HtS0=
# Reddit user Bakibol: https://www.reddit.com/r/adventofcode/comments/1phywvn/2025_day_9_solutions/


def parse_input(filename: str | pl.Path) -> list[list[int]]:
    with open(filename) as input_file:
        return [[int(num) for num in row.split(",")] for row in input_file.read().splitlines()]


def compress_coordinates(coordinates) -> list[tuple[int, int]]:
    x_values = [c[0] for c in coordinates]
    y_values = [c[1] for c in coordinates]
    unique_x, unique_y = sorted(set(x_values)), sorted(set(y_values))
    x_rank = {x: i for i, x in enumerate(unique_x)}
    y_rank = {y: i for i, y in enumerate(unique_y)}

    mapping = [(x_rank[x], y_rank[y]) for x, y in coordinates]
    return mapping


def span(c1: tuple[int, int], c2: tuple[int, int]) -> set[tuple[int, int]]:
    x1, y1 = c1
    x2, y2 = c2
    x_min, x_max = sorted((x1, x2))
    y_min, y_max = sorted((y1, y2))
    return {(x, y) for x in range(x_min, x_max + 1) for y in range(y_min, y_max + 1)}


def flood_fill(borders: set[tuple[int, int]], internal_point: tuple[int, int]) -> set[tuple[int, int]]:
    """
    Implements a flood fill algorithm to find all internal points starting from a seed point.
    The directions are up, down, left, right for a 2D grid.
    Importatnly, the internal_point must be inside the borders you want to fill.
    """
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    visited = set()
    queue = deque([internal_point])
    max_tries = 1_000_000
    tries = 0
    while queue and tries < max_tries:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        x, y = current

        # We add new points in all four directions if they are not within the borders
        # In other words, the borders define the area we cannot enter, or have to stay within
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) not in borders:
                queue.append((new_x, new_y))
        tries += 1
    return visited


def create_borders(coordinates: list[tuple[int, int]]) -> set[tuple[int, int]]:
    """Creates the border points of the full polygon defined by the given coordinates."""
    borders = set()
    complete = coordinates + [coordinates[0]]
    for c1, c2 in zip(complete, complete[1:]):
        borders.update(span(c1, c2))

    return borders


def calculate_area(rectangle: Sequence[Sequence[int]]) -> int:
    """Calculates the area of a rectangle defined by two points."""
    (x1, y1), (x2, y2) = rectangle
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def rectangle_inside(p1: tuple[int, int], p2: tuple[int, int], polygon: set[tuple[int, int]]) -> bool:
    """
    Checks if the rectangle defined by p1 and p2 is completely inside the polygon.

    :param p1: Description
    :type p1: tuple[int, int]
    :param p2: Description
    :type p2: tuple[int, int]
    :param polygon: Description
    :type polygon: set[tuple[int, int]]
    :return: Description
    :rtype: bool
    """
    x1, y1 = p1
    x2, y2 = p2
    x_min, x_max = sorted((x1, x2))
    y_min, y_max = sorted((y1, y2))

    # First check the corners
    corners = [(x_min, y_min), (x_min, y_max), (x_max, y_min), (x_max, y_max)]
    for corner in corners:
        if corner not in polygon:
            return False

    # Then check the edges
    for x in range(x_min, x_max + 1):
        if (x, y_min) not in polygon or (x, y_max) not in polygon:
            return False
    for y in range(y_min, y_max + 1):
        if (x_min, y) not in polygon or (x_max, y) not in polygon:
            return False
    return True


def part_two(coordinates: list[list[int]]) -> int:
    compressed = compress_coordinates(coordinates)

    borders = create_borders(compressed)
    interior_seed: tuple[int, int] = ((min(x for x, y in compressed) + max(x for x, y in compressed)) // 2, (min(y for x, y in compressed) + max(y for x, y in compressed)) // 2)
    plot_points(borders, point_size=3)
    interior = flood_fill(borders, interior_seed)
    plot_points(interior, point_size=3)
    polygon = borders | interior
    plot_points(polygon, point_size=3)

    max_area = 0
    for i, p1 in enumerate(compressed):
        for j, p2 in enumerate(compressed[i + 1 :], start=i + 1):
            area = calculate_area((coordinates[i], coordinates[j]))
            if area <= max_area:
                continue
            if rectangle_inside(p1, p2, polygon):
                max_area = area
    return max_area


def plot_points(points, point_size=2):
    xs, ys = zip(*points)
    plt.figure(figsize=(10, 10))
    plt.scatter(xs, ys, s=point_size)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()


def main():
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"

    coordinates = parse_input(example_file)
    # compressed = compress_coordinates(coordinates)
    # borders = create_borders(compressed)

    # plot_points(borders, point_size=100)
    print(part_two(coordinates))


if __name__ == "__main__":
    main()
