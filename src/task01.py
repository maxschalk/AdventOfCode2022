import itertools

from pathlib import Path
from contextlib import suppress

from PATHS import TEST_INPUT_DIR, TASK_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = TASK_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")


# SOLUTION


def _solve_part_one(data):
    def safe_parse(s):
        if s == "":
            return None
        
        return int(s)

    data = map(safe_parse, data)

    elves = (list(y) for x, y in itertools.groupby(data, lambda elem: elem is None) if not x)

    elves = sorted(map(sum, elves), reverse=True)

    return sum(elves[:3])


def _solve_part_two(data):
    raise NotImplementedError


# TASK-SPECIFIC BOILERPLATE


def solve_test(data):
    with suppress(NotImplementedError):
        print(f"Part 1 - {_solve_part_one(data)}")

        print("-" * 15)

        print(f"Part 2 - {_solve_part_two(data)}")


def solve(data):
    with suppress(NotImplementedError):
        solve_part_one(data)
        solve_part_two(data)


def solve_part_one(data):
    print(_solve_part_one(data))


def solve_part_two(data):
    print(_solve_part_two(data))


# GENERAL BOILERPLATE


def read_input(test: bool = False):
    path = TEST_INPUT_FILE if test else INPUT_FILE

    with open(path, "r") as file:
        content = file.read()

    return content.split("\n")


def main(test=False):
    data = read_input(test)

    if test:
        solve_test(data)
    else:
        solve(data)


if __name__ == "__main__":
    main()
