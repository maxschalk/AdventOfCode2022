import re
import string
from contextlib import suppress
from pathlib import Path

from PATHS import TASK_INPUT_DIR, TEST_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = TASK_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")


# SOLUTION


def neighbor_coords(row, col):
    return (
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    )


def _dyno(grid, start, memo):

    while (result := memo[start[0]][start[1]]) == -1:

        for row, grid_row in enumerate(grid):
            for col, grid_value in enumerate(grid_row):
                if memo[row][col] == -1:
                    continue

                for nrow, ncol in neighbor_coords(row, col):
                    try:
                        nval = grid[nrow][ncol]
                        nmemo = memo[nrow][ncol]
                    except IndexError:
                        continue

                    if nmemo == -1 and nval >= grid_value - 1:
                        memo[nrow][ncol] = memo[row][col] + 1

    return result


def _solve_part_one(data):
    coordinates, grid = data
    start, end = coordinates
    memo = [[-1] * len(grid[0]) for _ in range(len(grid))]
    memo[end[0]][end[1]] = 0
    return _dyno(grid, start, memo)


def _dyno_two(grid, memo):

    for _ in range(len(grid) * len(grid[0]) + 1):

        for row, grid_row in enumerate(grid):
            for col, grid_value in enumerate(grid_row):
                if memo[row][col] == -1:
                    continue

                for nrow, ncol in neighbor_coords(row, col):
                    try:
                        nval = grid[nrow][ncol]
                        nmemo = memo[nrow][ncol]
                    except IndexError:
                        continue

                    if nmemo == -1 and nval >= grid_value - 1:
                        memo[nrow][ncol] = memo[row][col] + 1


def _solve_part_two(data):
    coordinates, grid = data
    _, end = coordinates
    memo = [[-1] * len(grid[0]) for _ in range(len(grid))]
    memo[end[0]][end[1]] = 0

    _dyno_two(grid, memo)
    print(*memo, sep="\n")

    result = len(grid) * len(grid[0]) + 1

    for row, grid_row in enumerate(grid):
        for col, grid_value in enumerate(grid_row):
            if grid_value == 0 and memo[row][col] != -1:
                result = min(result, memo[row][col])

    return result


# TASK-SPECIFIC BOILERPLATE


def solve_part_one(grid):
    print(_solve_part_one(grid))


def solve_part_two(data):
    print(_solve_part_two(data))


def solve_test(data):
    with suppress(NotImplementedError):
        print(f"Part 1 - {_solve_part_one(data)}")

        print("-" * 15)

        print(f"Part 2 - {_solve_part_two(data)}")


def solve_test_individual_lines(data):
    with suppress(NotImplementedError):
        for line in data:
            print(f"Part 1: {line}: {_solve_part_one(line)}")

        print("-" * 30)

        for line in data:
            print(f"Part 2: {line}: {_solve_part_two(line)}")


def solve(data):
    with suppress(NotImplementedError):
        solve_part_one(data)
        solve_part_two(data)


# GENERAL BOILERPLATE


def read_input(test: bool = False):
    path = TEST_INPUT_FILE if test else INPUT_FILE

    with open(path, "r") as file:
        content = file.read()

    return content.split("\n")


GRID_TRANSLATE = {
    **{letter: ind for ind, letter in enumerate(string.ascii_lowercase)},
    "S": 0,
    "E": 25,
}


def parse_input(data):
    grid = tuple(
        tuple(map(lambda elem: GRID_TRANSLATE.get(elem, elem), line)) for line in data
    )

    start = None
    end = None

    for row, row_data in enumerate(data):
        for col, col_data in enumerate(row_data):
            if col_data == "S":
                start = (row, col)
            elif col_data == "E":
                end = (row, col)

    coordinates = (start, end)

    return coordinates, grid


def main(test=False):
    data = read_input(test)
    data = parse_input(data)

    if test:
        solve_test(data)
    else:
        solve(data)


if __name__ == "__main__":
    main(test=False)
