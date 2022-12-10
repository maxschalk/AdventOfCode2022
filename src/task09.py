import re

from pathlib import Path
from contextlib import suppress

from PATHS import TEST_INPUT_DIR, TASK_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = TASK_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")


# SOLUTION

DIRECTION_OFFSETS = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def step_head(state, direction, steps):
    offset = DIRECTION_OFFSETS[direction]

    state[0] += offset[0] * steps
    state[1] += offset[1] * steps


def sign(num):
    return (-1, 1)[num > 0]


def validate_state(head_xy, tail_xy):
    return abs(head_xy[0] - tail_xy[0]) < 2 and abs(head_xy[1] - tail_xy[1]) < 2


def step_tail(head_xy, tail_xy, visited):
    while not validate_state(head_xy, tail_xy):
        diff_xy = (head_xy[0] - tail_xy[0], head_xy[1] - tail_xy[1])

        if diff_xy[0] != 0:
            tail_xy[0] += sign(diff_xy[0])

        if diff_xy[1] != 0:
            tail_xy[1] += sign(diff_xy[1])

        visited[tuple(tail_xy)] = True


def _solve_part_one(data):
    head_xy = [0, 0]
    tail_xy = [0, 0]

    visited = {(0, 0): True}

    for direction, steps in data:
        step_head(head_xy, direction, steps)
        step_tail(head_xy, tail_xy, visited)

    return len(visited)


def _solve_part_two(data):
    head_xy = [0, 0]
    knots_xy = [[0, 0] for _ in range(9)]

    visiteds = [{(0, 0): True} for _ in range(9)]

    for direction, steps in data:
        for _ in range(steps):
            step_head(head_xy, direction, 1)

            head = head_xy
            for knot_xy, visited in zip(knots_xy, visiteds):
                step_tail(head, knot_xy, visited)
                head = knot_xy

    return len(visiteds[-1])


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


def parse_input(data):
    out = []

    pattern = re.compile(r"(?s)([RLUD]) (\d+)")

    for line in data:
        direction, step_count = pattern.match(line).groups()

        out.append((direction, int(step_count)))

    return out


def main(test=False):
    data = read_input(test)
    data = parse_input(data)

    if test:
        solve_test(data)
    else:
        solve(data)


if __name__ == "__main__":
    main(test=False)
