"""Module for practicing with the numpy einsum function."""

import numpy as np
from numpy.typing import NDArray

SUM_INDICES = "klmnopqrstuvwxyz"

SUBSCRIPT_LETTERS = "ijklmno"
SUPERSCRIPT_LETTERS = "pqrstuv"


def try_matrix_multiplication(a: NDArray, b: NDArray) -> None:
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
    print(einsum_subscript)

    result = np.einsum(einsum_subscript, a, b)
    print("Initial matrices")
    [print(arr) for arr in [a, b]]
    print("Matrix multiplication")
    print(result)


def try_transpose(a: NDArray) -> None:
    """
    Transposes a matrix using numpy's einsum function

    :param a: Description
    :type a: NDArray
    :return: Description
    :rtype: NDArray[Any]
    """
    transposed = np.einsum("ij -> ji", a)
    result = np.einsum("ij, jk -> ik", transposed, a)

    other_way = np.einsum("ji, jk -> ik", a, a)
    print("Initial matrix")
    print(a)
    print("Transposed matrix")
    print(transposed)
    print("Contracted A^T * A matrix")
    print(result)
    print(other_way)

    print(a.T @ a)


def try_outer_product(a: NDArray, b: NDArray) -> None:
    """
    Takes two vectors (rank-1 tensors) and creates a matrix (rank-2 tensor) by performing the outer-product

    :param a: First vector
    :type a: NDArray
    :param b: Second vector
    :type b: NDArray
    """
    result = np.einsum("i, j -> ij", a, b)
    print("Outer product with einsum")
    print(result)


def try_tensor_contraction(T: NDArray, v: NDArray) -> None:
    """
    Performs a tensor contraction between a 2x2x2 tensor (rank-3 tensor) and a vector

    M_ij = Sum_k [T_ijk * V_k]

    :param T: 2x2x2 tensor
    :type T: NDArray
    :param v: vector
    :type v: NDArray
    """
    result = np.einsum("ijk, k -> ij", T, v)
    print("Contracted 2x2x2 tensor by a vector")
    print(result)


def main():
    # Example usage of numpy einsum
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])

    try_transpose(a)

    a = np.array([1, 2])
    b = np.array([3, 4])

    try_outer_product(a, b)

    # Creating a 2x2x2 tensor
    tensor_2x2x2 = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    print("2x2x2 Tensor:")
    print(tensor_2x2x2)

    b = np.array([1, 2])

    try_tensor_contraction(tensor_2x2x2, b)


if __name__ == "__main__":
    main()
