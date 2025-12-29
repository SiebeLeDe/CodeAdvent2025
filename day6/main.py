import pathlib as pl
import numpy as np

from dataclasses import dataclass


@dataclass
class MathProblem:
    numbers: list[int]
    operation: str


def read_math_problems_file(file_path: pl.Path) -> list[MathProblem]:
    """
    Reads the file containing math problems and returns a list of MathProblem instances.

    The format of the file is expected to be:
    - The number of lines it the number of integers a problem has with the last line being the operation (e.g., +, -, *, /).
    - Each column is separated by empty space(s).

    Example:

    123 328  51 64
     45 64  387 23
      6 98  215 314
    *   +   *   +

    """
    problems: list[MathProblem] = []

    data = np.loadtxt(file_path, dtype=str)

    for col in data.T:
        numbers = [int(num) for num in col[:-1]]
        operation = col[-1]
        problems.append(MathProblem(numbers=numbers, operation=operation))

    return problems


def read_math_problems_file_cephalopod_math(file_path: pl.Path) -> list[MathProblem]:
    """
    Reads a file in a Cephalopod math format which should be read from right-to-left column-wise.

    For example:

    123 328  51 64
     45 64  387 23
      6 98  215 314
    *   +   *   +

    represents the following problems (from right to left):

    4 + 431 + 623
    175 + 581 + 32
    8 + 248 + 369
    356 + 24 + 100
    """
    lines = file_path.read_text().splitlines()

    operation_lines = lines[-1]
    number_lines = lines[:-1]

    # Now we go through each column from left to right and read the digits from top to bottom
    problems = []
    numbers = []
    current_index = len(number_lines[0]) - 1  # Start from the rightmost character
    while current_index >= 0:
        # Read numbers from top to bottom for this column
        number = [line[current_index] for line in number_lines if line[current_index] != " "]
        numbers.append(int("".join(number)))

        # When we encounter an operation sign, we finalize the current problem and start a new one by resetting numbers. Also, we skip one more character because of the whitespaces between differrent problems (columns).
        if (operation := operation_lines[current_index]) != " ":
            problems.append(MathProblem(numbers=numbers, operation=operation))
            numbers = []
            current_index -= 1  # Skip the operation character

        # Move to the next character to the left which will stop when the index is less than 0
        current_index -= 1
    return problems


def solve_math_problem(problem: MathProblem) -> int:
    """
    Solves a MathProblem instance and returns the result as an integer.
    Supported operations are +, -, *, /.
    """
    if problem.operation == "+":
        return sum(problem.numbers)
    elif problem.operation == "-":
        result = problem.numbers[0]
        for num in problem.numbers[1:]:
            result -= num
        return result
    elif problem.operation == "*":
        result = 1
        for num in problem.numbers:
            result *= num
        return result
    elif problem.operation == "/":
        result = problem.numbers[0]
        for num in problem.numbers[1:]:
            result //= num  # Integer division
        return result
    else:
        raise ValueError(f"Unsupported operation: {problem.operation}")


def main():
    current_dir = pl.Path(__file__).parent
    example_file = current_dir / "example.txt"
    input_file = current_dir / "input.txt"

    # example_problems = read_math_problems_file(example_file)
    example_problems = read_math_problems_file_cephalopod_math(example_file)
    solved_problems = [solve_math_problem(problem) for problem in example_problems]

    final_result = sum(solved_problems)
    print("Example Problems:")
    for problem in example_problems:
        print(problem)
    print(f"Final Result: {final_result}")


if __name__ == "__main__":
    main()

    print(5384 + 9348430852243)
