import pathlib as pl
import numpy as np
from numpy.typing import NDArray
from matplotlib import pyplot as plt
from matplotlib import animation


def read_printing_puzzle(file_path: pl.Path) -> NDArray:
    """
    Reads a file containing a matrix of symbols "." (empty space) and "@" (space occupied by rolls of paper) in which each line represents a row.
    1 is used to represent "@" and 0 for ".".
    """
    file_lines = file_path.read_text().strip().splitlines()
    matrix = []
    for line in file_lines:
        row = [1 if char == "@" else 0 for char in line]
        matrix.append(row)
    return np.array(matrix)


def get_convolved_matrix(matrix: NDArray, stencil: NDArray) -> NDArray:
    """
    Applies a stencil convolution over a given matrix.
    The stencil is a smaller matrix that is slid over the input matrix to perform element-wise multiplication and summation.
    This function handles edge cases by padding the input matrix with zeros.
    """
    padded_matrix = np.pad(matrix, pad_width=1, mode="constant", constant_values=0)
    convolved_matrix = np.zeros_like(matrix)

    for i in range(1, padded_matrix.shape[0] - 1):
        for j in range(1, padded_matrix.shape[1] - 1):
            sub_matrix = padded_matrix[i - 1 : i + 2, j - 1 : j + 2]
            convolved_value = np.sum(sub_matrix * stencil)
            convolved_matrix[i - 1, j - 1] = convolved_value

    return convolved_matrix


def determine_accessible_printing_area(printing_puzzle: NDArray, convolved_matrix: NDArray) -> int:
    """
    Determines the accessible printing area in the printing puzzle matrix.
    An area is considered accessible if it has less than 4 occupied neighbors (1s) and is itself occupied (1).
    8-directional neighbors are considered (N, NE, E, SE, S, SW, W, NW).
    Returns the total count of accessible areas

    Arguments:
        printing_puzzle -- A matrix representing the printing puzzle, where 1 indicates a roll of paper and 0 indicates empty space.
        convolved_matrix -- A matrix representing the count of occupied neighbors for each cell.
    Returns:
        The total accessible area for printing as an integer.
    """

    accessible_paper = np.count_nonzero((convolved_matrix < 4) & (printing_puzzle == 1))
    return int(accessible_paper)


def remove_accessible_papers(printing_puzzle: NDArray, convolved_matrix: NDArray) -> NDArray:
    """
    Removes accessible areas from the printing puzzle matrix by setting them to 0.
    An area is considered accessible if it has less than 4 occupied neighbors (1s) and is itself occupied (1).
    8-directional neighbors are considered (N, NE, E, SE, S, SW, W, NW).

    Arguments:
        printing_puzzle -- A matrix representing the printing puzzle, where 1 indicates a roll of paper and 0 indicates empty space.
        convolved_matrix -- A matrix representing the count of occupied neighbors for each cell.
    Returns:
        The updated printing puzzle matrix with accessible areas removed.
    """
    accessible_mask = (convolved_matrix < 4) & (printing_puzzle == 1)
    printing_puzzle[accessible_mask] = 0
    return printing_puzzle


def print_paper_area_matrix(matrix: np.ndarray, convolved_matrix: NDArray | None = None) -> None:
    """
    Prints the paper area matrix in a readable format. If the convolved matrix is provided, the paper that is accessible (less than 4 neighbors) is marked with the "x" symbol.
    """
    if convolved_matrix is not None:
        for i in range(matrix.shape[0]):
            row_str = ""
            for j in range(matrix.shape[1]):
                if matrix[i, j] == 1:
                    if convolved_matrix[i, j] < 4:
                        row_str += "x"
                    else:
                        row_str += "@"
                else:
                    row_str += "."
            print(row_str)
        return

    for row in matrix:
        row_str = "".join("@" if cell == 1 else "." for cell in row)
        print(row_str)


def plot_matrix(matrix: NDArray) -> None:
    """
    Plots the given matrix using matplotlib for visualization.
    """
    plt.imshow(matrix, cmap="Greys", interpolation="nearest")
    plt.colorbar()
    plt.show()


def animate_removal(matrices: list[NDArray], removed_per_iteration: NDArray, interval: int = 500) -> None:
    """
    Creates an animation of the removal process using matplotlib.

    Arguments:
        matrices -- A list of matrices representing the state at each step.
        interval -- Time in milliseconds between frames.
    """
    fig, ax = plt.subplots()

    def update(frame):
        ax.clear()
        ax.imshow(matrices[frame], cmap="Greys", interpolation="nearest")
        ax.set_title(f"Step {frame} - Removed: {removed_per_iteration[frame]} rolls of paper")

    ani = animation.FuncAnimation(fig, update, frames=len(matrices), interval=interval)  # type: ignore
    plt.show()
    ani.save("removal_animation.gif", writer="imagemagick")


def main():
    """
    From a given printing puzzle matrix, determines the accessible area for printing.
    This area is defined by its surrounding neighbors (8 options: N, NE, E, SE, S, SW, W, NW) and it is only accesible if less than 4 neighbors are occupied (1).
    For this to work, we apply the stencil convolution method to the matrix:
    - We define a 3x3 stencil with all values set to 1.
    - We add extra padding of 0s around the matrix to handle edge cases.
    - We convolve the stencil over the matrix to count the number of occupied neighbors for each cell.

    Finally, we count the number of cells that are accessible (i.e., have less than 4 occupied neighbors and are themselves occupied [by a roll of paper!]).

    Arguments:
        printing_puzzle -- A matrix representing the printing puzzle, where 1 indicates a roll of paper and 0 indicates empty space.
    Returns:
        The total accessible area for printing as an integer.
    """
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"

    printing_puzzle = read_printing_puzzle(input_file)
    print("Initial Paper State:")
    print_paper_area_matrix(printing_puzzle)

    stencil = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

    matrices = [printing_puzzle.copy()]

    accessible_paper = 100
    removed_per_iteration = np.zeros(1000, dtype=int)
    for i in range(1000):
        convolved_matrix = get_convolved_matrix(printing_puzzle, stencil)
        accessible_paper = determine_accessible_printing_area(printing_puzzle, convolved_matrix)

        if accessible_paper == 0:
            print("No more accessible areas found.")
            break

        removed_per_iteration[i] = accessible_paper
        print(f"{i:3d}: Current Accessible Area: {accessible_paper}")
        # print_paper_area_matrix(printing_puzzle, convolved_matrix)
        printing_puzzle = remove_accessible_papers(printing_puzzle, convolved_matrix)
        matrices.append(printing_puzzle.copy())

    # print("Final Paper State:")
    # print_paper_area_matrix(printing_puzzle)
    print(f"Total removed: {removed_per_iteration.sum()}")
    plot_matrix(printing_puzzle)
    animate_removal(matrices, removed_per_iteration, interval=300)


# 16923 is too low
# 17146 is too high

if __name__ == "__main__":
    main()
