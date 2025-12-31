"""Module for practicing with the numpy einsum function."""

import numpy as np
from numpy.typing import NDArray

SUM_INDICES = "klmnopqrstuvwxyz"

SUBSCRIPT_LETTERS = "ijklmno"
SUPERSCRIPT_LETTERS = "pqrstuv"


def try_matrix_multiplication(a: NDArray, b: NDArray) -> NDArray:
    """Performs matrix multiplication using numpy's einsum function.

    Args:
        a: A xD numpy array.
        b: A xD numpy array.

    Returns:
        A xD numpy array resulting from the matrix multiplication of a and b.
    """
    keep_indices = ["i", "j"]
    sum_indices = [SUM_INDICES[i] for i in range(a.ndim - 2)]

    einsum_subscript = "".join(keep_indices + sum_indices) + "," + "".join(sum_indices + ["j"])
    einsum_subscript += "->" + "".join(keep_indices)
    print(f"Einsum subscript: {einsum_subscript}")

    result = np.einsum(einsum_subscript, a, b)
    return result


def main():
    # Example usage of numpy einsum
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])

    # Using einsum to perform matrix multiplication
    print("Matrix multiplication using einsum:")
    y = try_matrix_multiplication(a, b)
    print(y)

    # Check
    y = a @ b
    print(y)


if __name__ == "__main__":
    main()
