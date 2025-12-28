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
        print(numbers)
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
    lines = []
    with open(file_path, "r") as f:
        lines = f.readlines()

    operation_lines = lines[-1]
    number_lines = lines[:-1]

    [print(line) for line in lines]

    # The operation sign defines the last digit of each column
    operation_indices = [i for i, char in enumerate(operation_lines) if char.strip()]
    # The minus one accounts for the whitespace that separates each math problem / column
    n_numbers_per_problem = [operation_indices[i] - operation_indices[i - 1] - 1 for i in range(1, len(operation_indices))]
    print(f"Operation indices: {operation_indices[:10]}")
    print(f"Numbers per problem: {n_numbers_per_problem[:10]}")

    # Now we go through each column from left to right and read the digits from top to bottom
    problems = []
    current_index = 0
    for i, n_digits in enumerate(n_numbers_per_problem):
        numbers = []

        for i in range(n_digits):
            number = []
            for line in number_lines:
                char = line[current_index + i]
                if char.strip():
                    number.append(int(char))
            numbers.append(int("".join(map(str, number))))

        operation = operation_lines[current_index]
        problems.append(MathProblem(numbers=numbers, operation=operation))
        current_index += n_digits + 1  # Move to the next problem, accounting for whitespace

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
    example_problems = read_math_problems_file_cephalopod_math(input_file)
    solved_problems = [solve_math_problem(problem) for problem in example_problems]

    final_result = sum(solved_problems)
    print("Example Problems:")
    for problem in example_problems:
        print(problem)
    print(f"Final Result: {final_result}")


if __name__ == "__main__":
    main()

    print(5384 + 9348430852243)
