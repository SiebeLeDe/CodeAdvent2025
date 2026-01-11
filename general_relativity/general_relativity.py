from attrs import define
import sympy as sp
from typing import Protocol, Sequence
import itertools

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

    $\Gamma^{\alpha}_{\beta \gamma} = \frac{1}{2} g^{\alpha \epsilon} \left( \partial_{\gamma} g_{\beta \epsilon} + \partial_{\beta} g_{\gamma \epsilon} - \partial_{\epsilon} g_{\beta \gamma} \right)$

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
                    first_term = sp.diff(metric[beta, epsilon], symbols[gamma])
                    second_term = sp.diff(metric[gamma, epsilon], symbols[beta])
                    third_term = sp.diff(metric[beta, gamma], symbols[epsilon])
                    # Sum the terms and multiply by the inverse metric
                    Gamma[alpha, beta, gamma] += g_inv[alpha, epsilon] * (first_term + second_term - third_term)  # type: ignore

                Gamma[alpha, beta, gamma] = 0.5 * Gamma[alpha, beta, gamma].simplify()
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
                    Riemann[alpha, beta, gamma, delta] = Riemann[alpha, beta, gamma, delta].simplify()

    return Riemann


def ricci_tensor(Riemann: sp.Matrix) -> sp.Matrix:
    """
    Calculates the Ricci tensor by contracting the Riemann curvature tensor along its first and third indices (1st: contravariant, 3rd: covariant).
    The Ricci tensor provides a measure of the degree to which the volume of a small geodesic ball in a curved space deviates from that in flat space.
    """
    n = Riemann.shape[0]
    Ricci = sp.MutableDenseNDimArray.zeros(n, n)

    for alpha in range(n):
        for beta in range(n):
            Ricci[alpha, beta] = sum(Riemann[epsilon, alpha, epsilon, beta] for epsilon in range(n))  # type: ignore
            Ricci[alpha, beta]
    return Ricci


def ricci_scalar(Ricci: sp.Matrix, inv_metric: sp.Matrix) -> sp.Expr:
    """
    Calculates the Ricci scalar by contracting the Ricci tensor with the inverse metric tensor.
    The Ricci scalar provides a single scalar value that summarizes the curvature of space at a point.
    """
    n = Ricci.shape[0]
    R: sp.Expr = sum(inv_metric[alpha, beta] * Ricci[alpha, beta] for alpha in range(n) for beta in range(n))  # type: ignore
    R.simplify()
    return R


# ============================================================
# Printing functions
# ============================================================


def print_tensor(tensor: sp.Matrix, symbols: Sequence[sp.Symbol], header: str | None = None) -> None:
    """
    Prints a tensor in a readable format.

    If rank is >2, we flatten it down to 2D slices for each combination of the other indices.
    If rank is 2 or lower, we print it directly as a matrix/vector/scalar.
    """
    rank = tensor.rank()
    if rank <= 2:
        print(f"\n{header:=^50}\n") if header else None
        sp.pprint(tensor)
        return

    n = len(symbols)
    print(f"\n{header:=^50}\n") if header else None
    for indices in itertools.product(range(n), repeat=rank - 2):
        symbolic_matrix = sp.Matrix([[f"{''.join(str(symbols[i]) for i in indices)}" for _ in range(n)] for _ in range(n)])
        value_matrix = sp.Matrix([[tensor[indices + (i, j)] for j in range(n)] for i in range(n)])

        symbols_str = ", ".join(f"{symbols[idx]}={idx}" for idx, _ in enumerate(indices))
        print(f"Tensor for indices {symbols_str}:")
        sp.pprint(symbolic_matrix)
        sp.pprint(value_matrix)
        print()


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
    print("Ricci Scalar:\n")
    sp.pprint(ricci_scal)

    sp.pprint(riemann_tensor)


if __name__ == "__main__":
    main()
