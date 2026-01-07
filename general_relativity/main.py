# Main sympy_exercises for practicing with sympy in the context of general relativity.
# https://chatgpt.com/share/695e8302-bba0-800e-b62b-5c4070667073
import sympy as sp


def sympy_exercise_1():
    """Goal is to define symbols and use different expressions for sympy"""
    a, x, y = sp.symbols("a x y")
    f = a * x**2 * y + sp.sin(x * y)
    print(f"Original expression: {f}")
    f_sub = f.subs(a, 2)
    print(f"a = 2 substitution:  {f_sub}")
    print("\n\n")


def sympy_exercise_2():
    """Goal is to take a derivate and simplify the result"""
    a, x, y = sp.symbols("a x y")
    f = a * x**2 * y + sp.sin(x * y)

    df_dx = sp.diff(f, x)
    df_dy = sp.diff(f, y)
    d2f_dx2 = sp.diff(f, x)

    df_dx_s = sp.simplify(df_dx)
    df_dy_s = sp.simplify(df_dy)
    d2f_dx2_s = sp.simplify(d2f_dx2)

    print(f"Original expression: {f}")

    print("\nDerivatives")
    print(f"x-derivative: {df_dx}")
    print(f"y-derivative: {df_dy}")
    print(f"2nd x-derivative: {d2f_dx2}")

    print("\nSimplified expressions")
    print(f"x-derivative: {df_dx_s}")
    print(f"y-derivative: {df_dy_s}")
    print(f"2nd x-derivative: {d2f_dx2_s}")


def sympy_exercise_3():
    x, y = sp.symbols("x y")
    vector = sp.Matrix(
        [
            x**2,
            x * y,
            sp.sin(y),
        ]
    )

    matrix = sp.Matrix(
        [
            [x, y],
            [y, x],
        ]
    )
    sp.pretty_print(matrix)

    product = matrix * vector[:2, :]
    print(product)
    print(matrix.det())
    print(matrix.inv())


def sympy_exercise_4():
    pass


def sympy_exercise_5():
    pass


def sympy_exercise_6():
    pass


def main():
    sympy_exercise_1()
    sympy_exercise_2()
    sympy_exercise_3()
    sympy_exercise_4()
    sympy_exercise_5()
    sympy_exercise_6()


if __name__ == "__main__":
    main()
