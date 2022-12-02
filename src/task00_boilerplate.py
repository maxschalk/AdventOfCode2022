import re

from pathlib import Path
from contextlib import suppress

from PATHS import TEST_INPUT_DIR, TASK_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = TASK_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")


# SOLUTION


def _solve_part_one(data):
    print(data)


def _solve_part_two(data):
    raise NotImplementedError


# TASK-SPECIFIC BOILERPLATE


def solve_part_one(data):
    print(_solve_part_one(data))


def solve_part_two(data):
    print(_solve_part_two(data))


def solve_test(data):
    with suppress(NotImplementedError):
        print(f"Part 1 - {solve_part_one(data)}")

        print("-" * 15)

        print(f"Part 2 - {solve_part_two(data)}")


def solve_test_individual_lines(data):
    with suppress(NotImplementedError):
        for line in data:
            print(f"Part 1: {line}: {solve_part_one(line)}")

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


def parse_input(data, test: bool = False):
    out = []

    pattern = re.compile(r"(?s)(.+)")

    for line in data:
        result = pattern.match(line).groups()

        out.append(result)

    return out


def main(test=False):
    data = read_input(test)
    data = parse_input(data, test)

    if test:
        solve_test(data)
    else:
        solve(data)


if __name__ == "__main__":
    main()
