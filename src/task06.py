from collections import deque

from pathlib import Path
from contextlib import suppress

from PATHS import TEST_INPUT_DIR, TASK_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = TASK_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")


# SOLUTION


def _solve(data, marker_len):
    data_iter = iter(data)

    window = deque()

    for _ in range(marker_len):
        window.append(next(data_iter))

    if len(set(window)) == marker_len:
        return marker_len

    for i, elem in enumerate(data_iter, start=marker_len + 1):
        window.popleft()
        window.append(elem)

        if len(set(window)) == marker_len:
            return i

    return len(data)


def _solve_part_one(data):
    return _solve(data, 4)


def _solve_part_two(data):
    return _solve(data, 14)


# TASK-SPECIFIC BOILERPLATE


def solve_part_one(data):
    print(_solve_part_one(data))


def solve_part_two(data):
    print(_solve_part_two(data))


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

    return content


def main(test=False):
    data = read_input(test)

    if test:
        solve_test_individual_lines(data)
    else:
        solve(data)


if __name__ == "__main__":
    main(test=False)
