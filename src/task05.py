import re
from collections import defaultdict, deque

from pathlib import Path
from contextlib import suppress

from PATHS import TEST_INPUT_DIR, TASK_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = TASK_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")


# SOLUTION


def _solve_part_one(data):
    cargo, moves = data

    for quant, from_stack, to_stack in moves:
        for _ in range(quant):
            cargo[to_stack].append(cargo[from_stack].pop())

    return str.join(
        "", map(lambda t: t[1], sorted(map(lambda t: (t[0], t[1][-1]), cargo.items())))
    )


def _solve_part_two(data):
    cargo, moves = data

    for quant, from_stack, to_stack in moves:
        temp = deque()
        for _ in range(quant):
            temp.appendleft(cargo[from_stack].pop())

        cargo[to_stack].extend(temp)

    return str.join(
        "", map(lambda t: t[1], sorted(map(lambda t: (t[0], t[1][-1]), cargo.items())))
    )


# TASK-SPECIFIC BOILERPLATE


def solve_part_one(data):
    print(_solve_part_one(data))


def solve_part_two(data):
    print(_solve_part_two(data))


def solve_test(data):
    with suppress(NotImplementedError):
        # print(f"Part 1 - {_solve_part_one(data)}")

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
        # solve_part_one(data)
        solve_part_two(data)


# GENERAL BOILERPLATE


def read_input(test: bool = False):
    path = TEST_INPUT_FILE if test else INPUT_FILE

    with open(path, "r") as file:
        content = file.read()

    return content.split("\n")


def parse_input(data):

    iter_data = iter(data)

    cargo = defaultdict(deque)

    for line in iter_data:
        if line == "":
            break

        cargoline = line[1::4]

        if str.isnumeric(cargoline):
            continue

        for ind, letter in enumerate(cargoline, start=1):
            if letter == " ":
                continue

            cargo[ind].appendleft(letter)

    moves = []

    move_pattern = re.compile(r"(?s)move (\d+) from (\d+) to (\d+)")

    for line in iter_data:
        result = move_pattern.match(line).groups()

        moves.append(tuple(map(int, result)))

    return dict(cargo), moves


def main(test=False):
    data = read_input(test)
    data = parse_input(data)

    if test:
        solve_test(data)
    else:
        solve(data)


if __name__ == "__main__":
    main(test=False)
