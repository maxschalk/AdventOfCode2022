import re

from pathlib import Path
from contextlib import suppress

from PATHS import TEST_INPUT_DIR, TASK_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = TASK_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")


# SOLUTION


def is_visible(grid, row, col, max_row, max_col):
    if all(grid[row][x] < grid[row][col] for x in range(0, col)):
        return True

    if all(grid[row][x] < grid[row][col] for x in range(col + 1, max_col)):
        return True

    if all(grid[y][col] < grid[row][col] for y in range(0, row)):
        return True

    if all(grid[y][col] < grid[row][col] for y in range(row + 1, max_row)):
        return True

    return False


def _solve_part_one(data):
    max_y = len(data)
    max_x = len(data[0])

    return sum(
        int(is_visible(data, y, x, max_y, max_x))
        for y in range(0, max_y)
        for x in range(0, max_x)
    )


def view_score(grid, row, col):
    left = 0
    for x in range(col - 1, -1, -1):
        left += 1
        if grid[row][x] >= grid[row][col]:
            break

    right = 0
    for x in range(col + 1, len(grid[0])):
        right += 1
        if grid[row][x] >= grid[row][col]:
            break

    top = 0
    for y in range(row - 1, -1, -1):
        top += 1
        if grid[y][col] >= grid[row][col]:
            break

    bottom = 0
    for y in range(row + 1, len(grid)):
        bottom += 1
        if grid[y][col] >= grid[row][col]:
            break

    return left * right * top * bottom


def _solve_part_two(data):
    def grid_coords(grid):
        for y in range(0, len(data)):
            for x in range(0, len(data[0])):
                yield y, x

    return max(map(lambda coords: view_score(data, *coords), grid_coords(data)))


# TASK-SPECIFIC BOILERPLATE


def solve_part_one(data):
    print(_solve_part_one(data))


def solve_part_two(data):
    print(_solve_part_two(data))


def solve_test(data):
    with suppress(NotImplementedError):
        print(f"Part 1 - {_solve_part_one(data)}")

        print("-" * 15)

        print(f"Part 2 - {_solve_part_two(data)}")


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


def main(test=False):
    data = read_input(test)
    data = tuple(map(lambda r: tuple(map(int, r)), data))

    if test:
        solve_test(data)
    else:
        solve(data)


if __name__ == "__main__":
    main(test=False)
