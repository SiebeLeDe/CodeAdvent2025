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
    """
    Calculates the Christoffel symbols of the second kind for a given metric tensor.
    These are also known as the Levi-Civita connection coefficients and represent how the basis vectors change from two nearby points in a curved space (infinitesimally small displacements).
    In a flat space, all Christoffel symbols are zero which one may verify using Cartesian coordinates, polar coordinates or spherical coordinates.
    """

    n = metric.shape[0]
    inv_metric = metric.inv()
    Gamma = sp.MutableDenseNDimArray.zeros(n, n, n)

    for alpha in range(n):
        for beta in range(n):
            for gamma in range(n):
                # Compute the Christoffel symbol components
                first_term = sp.diff(metric[beta, gamma], symbols[alpha])
                second_term = sp.diff(metric[alpha, gamma], symbols[beta])
                third_term = sp.diff(metric[alpha, beta], symbols[gamma])
                # Sum the terms and multiply by the inverse metric
                Gamma[alpha, beta, gamma] = 0.5 * sum(inv_metric[alpha, epsilon] * (first_term + second_term - third_term) for epsilon in range(n))  # type: ignore
                Gamma[alpha, beta, gamma].simplify()
    return Gamma


def print_christoffel_symbols(Gamma: sp.Matrix, symbols: Sequence[sp.Symbol]) -> None:
    """
    Prints the Christoffel symbols in a readable format:

    [Matrix containing symbol notation]  = [Gamma matrix component] for each summed index

    Example output for spherical coordinates:

    [
        [Γ^r_{r, r}, Γ^r_{r, θ}, Γ^r_{r, φ}],
        [Γ^θ_{r, r}, Γ^θ_{r, θ}, Γ^θ_{r, φ}],
        [Γ^φ_{r, r}, Γ^φ_{r, θ}, Γ^φ_{r, φ}]
    ] =
    [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    """
    n = len(symbols)
    for alpha in range(n):
        # Create a symbolic matrix for the Christoffel symbols for this alpha
        symbolic_matrix = sp.Matrix([[f"{str(symbols[alpha])}{str(symbols[beta])}{str(symbols[gamma])}" for gamma in range(n)] for beta in range(n)])
        # Create a matrix for the corresponding computed values
        value_matrix = sp.Matrix([[Gamma[alpha, beta, gamma] for gamma in range(n)] for beta in range(n)])

        # Pretty print the symbolic matrix and its corresponding values
        print(f"Christoffel Symbols for Γ^{symbols[alpha]}:")
        sp.pprint(symbolic_matrix)
        sp.pprint(value_matrix)
        print("\n")


# ============================================================
# Main function to demonstrate the usage
# ============================================================


def main():
    coords = SchwarzschildCoordinateSystem()
    Gamma = christoffel_symbols(coords.metric_tensor, coords.symbols)

    sp.pprint(coords.metric_tensor)
    print_christoffel_symbols(Gamma, coords.symbols)


if __name__ == "__main__":
    main()
