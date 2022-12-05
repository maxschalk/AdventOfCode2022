import re
import string

from pathlib import Path
from contextlib import suppress

from PATHS import TEST_INPUT_DIR, TASK_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = TASK_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")


# SOLUTION

PRIORITIES = {
    letter: p + 1
    for p, letter in enumerate((*string.ascii_lowercase, *string.ascii_uppercase))
}


def split_string_halves(s):
    str_len = len(s)
    return s[: str_len // 2], s[str_len // 2 :]


def get_duplicate(backpack):
    comp1, comp2 = backpack

    duplicates = set(comp1).intersection(comp2)

    dup, *rest = duplicates

    assert len(rest) == 0

    return dup


def _solve_part_one(data):
    backpacks = map(split_string_halves, data)

    duplicates = map(get_duplicate, backpacks)

    return sum(PRIORITIES[item] for item in duplicates)


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def get_multi_intersection(iterables):
    item, *iterables = iterables

    res = set(item)

    for i in iterables:
        res = res.intersection(set(i))

    assert len(res) == 1

    item, *rest = res

    return item


def _solve_part_two(data):
    backpack_groups = chunks(data, 3)

    tags = map(get_multi_intersection, backpack_groups)

    return sum(PRIORITIES[item] for item in tags)


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


def main(test=False):
    data = read_input(test)

    if test:
        solve_test(data)
    else:
        solve(data)


if __name__ == "__main__":
    main(test=False)
