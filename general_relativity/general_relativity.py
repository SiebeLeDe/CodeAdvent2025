"""
This module provides functions to compute fundamental quantities in General Relativity, including:

1. **Metric Tensor**: Describes the geometry of spacetime and encodes information about distances and angles.
2. **Christoffel Symbols**: Represent the connection coefficients that describe how vectors change as they are parallel transported.
3. **Riemann Curvature Tensor**: Measures the curvature of spacetime and how much it deviates from being flat.
4. **Ricci Tensor**: A contraction of the Riemann tensor, summarizing curvature information relevant to Einstein's field equations.
5. **Ricci Scalar**: A single scalar value summarizing the curvature of spacetime at a point.

Functions:
- `christoffel_symbols`: Computes the Christoffel symbols of the second kind.
- `riemann_curvature_tensor`: Computes the Riemann curvature tensor.
- `ricci_tensor`: Computes the Ricci tensor by contracting the Riemann tensor.
- `ricci_scalar`: Computes the Ricci scalar by contracting the Ricci tensor with the inverse metric.
- `print_tensor` and `print_riemann_curvature_tensor`: Utility functions for displaying tensors in a readable format.

"""

from attrs import define
import sympy as sp
from typing import Protocol, Sequence

sp.init_printing(use_latex=True)


class CoordinateSystem(Protocol):
    metric_tensor: sp.Matrix
    symbols: list[sp.Symbol]


@define
class PolarCoordinateSystem(CoordinateSystem):
    r, theta = sp.symbols("r θ", real=True, positive=True)

    metric_tensor = sp.Matrix([[1, 0], [0, r**2]])
    symbols = [r, theta]


@define
class Sphere2DCoordinateSystem(CoordinateSystem):
    r, theta, phi = sp.symbols("r θ, φ", real=True, positive=True)

    metric_tensor = sp.Matrix(
        [
            [r**2, 0],
            [0, r**2 * sp.sin(theta) ** 2],  # type: ignore
        ]
    )
    symbols = [theta, phi]


@define
class SphericalCoordinateSystem(CoordinateSystem):
    r, theta, phi = sp.symbols("r θ φ", real=True, positive=True, cls=sp.Symbol)

    metric_tensor = sp.Matrix(
        [
            [1, 0, 0],
            [0, r**2, 0],
            [0, 0, r**2 * sp.cos(theta) ** 2],  # type: ignore
        ]
    )
    symbols = [r, theta, phi]


@define
class SchwarzschildCoordinateSystem(CoordinateSystem):
    t, r, theta, phi = sp.symbols("t r θ φ", real=True, positive=True, cls=sp.Symbol)
    M = sp.symbols("M", real=True, positive=True, cls=sp.Symbol)

    metric_tensor = sp.Matrix(
        [
            [1 - (2 * M) / r, 0, 0, 0],
            [0, -1 / (1 - (2 * M) / r), 0, 0],
            [0, 0, -(r**2), 0],
            [0, 0, 0, -(r**2) * sp.sin(theta) ** 2],  # type: ignore
        ]
    )
    symbols = [t, r, theta, phi]


# ============================================================
# Christoffel Symbols using the metric tensor
# ============================================================


def christoffel_symbols(metric: sp.Matrix, symbols: Sequence[sp.Symbol]) -> sp.Matrix:
    r"""
    Calculates the Christoffel symbols of the second kind for a given metric tensor.
    These are also known as the Levi-Civita connection coefficients and represent how the basis vectors change from two nearby points in a curved space (infinitesimally small displacements).
    In a flat space, all Christoffel symbols are zero which one may verify using Cartesian coordinates, polar coordinates or spherical coordinates.

    \Gamma^{i}_{jk} = \frac{1}{2} g^{il} \left( \partial_{k} g_{lj} + \partial_{j} g_{lk} - \partial_{l} g_{jk} \right)

    or using the index notation:
    i = alpha
    j = beta
    k = gamma

    \Gamma^{\alpha}_{\beta \gamma} = \frac{1}{2} g^{\alpha \epsilon} \left( \partial_{\gamma} g_{\epsilon \beta} + \partial_{\beta} g_{\epsilon \gamma} - \partial_{\epsilon} g_{\beta \gamma} \right)

    Parameters:
    - metric (sp.Matrix): The metric tensor, a symmetric matrix representing spacetime geometry.
    - symbols (Sequence[sp.Symbol]): The coordinate symbols (e.g., t, x, y, z).

    Returns:
    - sp.Matrix: A 3D array of Christoffel symbols \( \Gamma^i_{jk} \).
    """

    n = metric.shape[0]
    g_inv = metric.inv()
    Gamma = sp.MutableDenseNDimArray.zeros(n, n, n)

    for alpha in range(n):
        for beta in range(n):
            for gamma in range(n):
                Gamma[alpha, beta, gamma] = 0

                for epsilon in range(n):
                    # Compute the Christoffel symbol components
                    first_term = sp.diff(metric[epsilon, beta], symbols[gamma])
                    second_term = sp.diff(metric[epsilon, gamma], symbols[beta])
                    third_term = sp.diff(metric[beta, gamma], symbols[epsilon])
                    # Sum the terms and multiply by the inverse metric
                    Gamma[alpha, beta, gamma] += g_inv[alpha, epsilon] * (first_term + second_term - third_term)  # type: ignore

                Gamma[alpha, beta, gamma] = 0.5 * Gamma[alpha, beta, gamma]
    return Gamma


# ============================================================
# Riemann Curvature Tensor, Ricci Tensor, and Ricci Scalar
# ============================================================


def riemann_curvature_tensor(Gamma: sp.Matrix, symbols: Sequence[sp.Symbol]) -> sp.Matrix:
    r"""
    Calculates the Riemann curvature tensor from the Christoffel symbols.
    The Riemann curvature tensor measures the extent to which the metric tensor is not locally isometric to that of Euclidean space.

    R^{i}_{jlm} = \partial_{l} \Gamma^{i}_{mj} - \partial_{m} \Gamma^{i}_{lj} + \Gamma^{k}_{mj} \Gamma^{i}_{lk} - \Gamma^{k}_{lj} \Gamma^{i}_{km}

    or using the index notation:
    i = alpha
    j = beta
    l = gamma
    m = delta

    R^{\alpha}_{\beta \gamma \delta} = \partial_{\gamma} \Gamma^{\alpha}_{\beta \delta} - \partial_{\delta} \Gamma^{\alpha}_{\beta \gamma} + \Gamma^{\epsilon}_{\beta \delta} \Gamma^{\alpha}_{\epsilon \gamma} - \Gamma^{\epsilon}_{\beta \gamma} \Gamma^{\alpha}_{\epsilon \delta}

    Parameters:
    - Gamma (sp.Matrix): The Christoffel symbols of the second kind.
    - symbols (Sequence[sp.Symbol]): The coordinate symbols.

    Returns:
    - sp.Matrix: A 4D array representing the Riemann curvature tensor \( R^i_{jkl} \).
    """
    n = len(symbols)
    Riemann = sp.MutableDenseNDimArray.zeros(n, n, n, n)

    for alpha in range(n):
        for beta in range(n):
            for gamma in range(n):
                for delta in range(n):
                    term1: sp.Derivative = sp.diff(Gamma[alpha, beta, delta], symbols[gamma])
                    term2: sp.Derivative = sp.diff(Gamma[alpha, beta, gamma], symbols[delta])

                    term3 = 0
                    for epsilon in range(n):
                        term3 += Gamma[alpha, epsilon, gamma] * Gamma[epsilon, beta, delta] - Gamma[alpha, epsilon, delta] * Gamma[epsilon, beta, gamma]  # type: ignore

                    Riemann[alpha, beta, gamma, delta] = term1 - term2 + term3  # type: ignore

    return Riemann


def ricci_tensor(Riemann: sp.Matrix) -> sp.Matrix:
    """
    Calculates the Ricci tensor by contracting the Riemann curvature tensor along its first and third indices (1st: contravariant, 3rd: covariant).
    The Ricci tensor provides a measure of the degree to which the volume of a small geodesic ball in a curved space deviates from that in flat space.

    Parameters:
    - Riemann (sp.Matrix): The Riemann curvature tensor.

    Returns:
    - sp.Matrix: The Ricci tensor, a 2D array obtained by contracting the Riemann tensor.
    """
    n = Riemann.shape[0]
    Ricci = sp.MutableDenseNDimArray.zeros(n, n)

    for alpha in range(n):
        for beta in range(n):
            Ricci[alpha, beta] = 0
            for epsilon in range(n):
                Ricci[alpha, beta] += Riemann[epsilon, alpha, epsilon, beta]  # type: ignore
    return Ricci


def ricci_scalar(Ricci: sp.Matrix, inv_metric: sp.Matrix) -> sp.Symbol:
    """
    Calculates the Ricci scalar by contracting the Ricci tensor with the inverse metric tensor.
    The Ricci scalar provides a single scalar value that summarizes the curvature of space at a point.

    Parameters:
    - Ricci (sp.Matrix): The Ricci tensor.
    - inv_metric (sp.Matrix): The inverse of the metric tensor.

    Returns:
    - sp.Symbol: The Ricci scalar, a single value summarizing spacetime curvature.
    """
    n = Ricci.shape[0]
    R = sp.S.Zero

    for alpha in range(n):
        for beta in range(n):
            R += inv_metric[alpha, beta] * Ricci[alpha, beta]  # type: ignore
    return R


# ============================================================
# Printing functions
# ============================================================


def print_tensor(tensor: sp.Matrix, symbols: Sequence[sp.Symbol], header: str = "Tensor"):
    r"""
    Prints a general tensor in a readable format.

    Parameters:
    - tensor (sp.Matrix): The tensor to be printed.
    - symbols (Sequence[sp.Symbol]): The coordinate symbols.
    - header (str): A header for the printed output.

    Returns:
    - None
    """
    n = len(symbols)
    print(f"\n{header:=^60}:\n")
    simplified_tensor = tensor.applyfunc(sp.simplify)
    if tensor.rank() == 2:
        sp.pprint(simplified_tensor, use_unicode=True)
    elif tensor.rank() == 3:
        for alpha in range(n):
            print(f"\nSlice {alpha} ({symbols[alpha]}) with indices [{alpha}, :, :]:\n")
            sp.pprint(simplified_tensor[alpha, :, :], use_unicode=True)
    elif tensor.rank() == 4:
        for alpha in range(n):
            for beta in range(n):
                print(f"\nSlice [{alpha}, {beta}, :, :] ({symbols[alpha]}, {symbols[beta]}):\n")
                sp.pprint(simplified_tensor[alpha, beta, :, :], use_unicode=True)


def print_riemann_curvature_tensor(Riemann: sp.Matrix, symbols: Sequence[sp.Symbol], header: str = "Riemann Curvature Tensor"):
    r"""
    Prints the Riemann curvature tensor in a readable format.

    Parameters:
    - Riemann (sp.Matrix): The Riemann curvature tensor to be printed.
    - symbols (Sequence[sp.Symbol]): The coordinate symbols.
    - header (str): A header for the printed output.

    Returns:
    - None
    """
    n = len(symbols)
    print(f"\n{header}:\n")
    for alpha in range(n):
        for gamma in range(n):
            sp.pprint(Riemann[alpha, :, gamma, :], use_unicode=True)


# ============================================================
# Main function to demonstrate the usage
# ============================================================


def main():
    coords = Sphere2DCoordinateSystem()
    Gamma = christoffel_symbols(coords.metric_tensor, coords.symbols)

    print_tensor(coords.metric_tensor, coords.symbols, header="Metric Tensor in Polar Coordinates")

    riemann_tensor = riemann_curvature_tensor(Gamma, coords.symbols)
    ricci_tens = ricci_tensor(riemann_tensor)
    ricci_scal = ricci_scalar(ricci_tens, coords.metric_tensor.inv())

    print_tensor(Gamma, coords.symbols, header="Christoffel Symbols")
    print_tensor(riemann_tensor, coords.symbols, header="Riemann Curvature Tensor")
    print_tensor(ricci_tens, coords.symbols, header="Ricci Tensor")
    print(f"\n{'Ricci Scalar':=^60}:\n")
    sp.pprint(sp.simplify(ricci_scal), use_unicode=True)


if __name__ == "__main__":
    main()
