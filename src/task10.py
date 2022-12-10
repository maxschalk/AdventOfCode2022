import re

from pathlib import Path
from contextlib import suppress

from PATHS import TEST_INPUT_DIR, TASK_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = TASK_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")


# SOLUTION


def _solve_part_one(data):
    registers = {"X": 1}
    cycle = 0
    cmd_buffer = None

    data_iter = iter(data)

    signals = []

    while cycle < 220:
        if cmd_buffer is not None:
            cycles_left, buffered = cmd_buffer

            if cycles_left == 0:
                _, arg = buffered
                registers["X"] += arg

                cmd_buffer = None

            else:
                cmd_buffer = (cycles_left - 1, buffered)

        if cmd_buffer is None:
            try:
                cmd, arg = next(data_iter)

                if cmd == "addx":
                    cmd_buffer = (1, (cmd, arg))

            except StopIteration:
                pass

        cycle += 1

        if cycle % 40 == 20:
            signals.append(cycle * registers["X"])

    return sum(signals)


def _solve_part_two(data):
    registers = {"X": 1}
    cycle = 0
    cmd_buffer = None

    data_iter = iter(data)

    output = [["."] * 40 for _ in range(6)]

    while cycle < 240:
        if cmd_buffer is not None:
            cycles_left, buffered = cmd_buffer

            if cycles_left == 0:
                _, arg = buffered
                registers["X"] += arg

                cmd_buffer = None

            else:
                cmd_buffer = (cycles_left - 1, buffered)

        if cmd_buffer is None:
            try:
                cmd, arg = next(data_iter)

                if cmd == "addx":
                    cmd_buffer = (1, (cmd, arg))

            except StopIteration:
                pass

        if cycle % 40 in range(registers["X"] - 1, registers["X"] + 2):
            output[cycle // 40][cycle % 40] = "#"

        cycle += 1

    return str.join("\n", map(lambda line: str.join("", line), output))


# TASK-SPECIFIC BOILERPLATE


def solve_part_one(data):
    print(_solve_part_one(data))


def solve_part_two(data):
    print(_solve_part_two(data))


def solve_test(data):
    with suppress(NotImplementedError):
        print(f"Part 1 - {_solve_part_one(data)}")

        print("-" * 15)

        print("Part 2:", _solve_part_two(data), sep="\n")


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

    pattern = re.compile(r"(?s)(noop)|((addx) (-?\d+))")

    for line in data:
        cmd1, _, cmd2, arg2 = pattern.match(line).groups()

        if cmd1 is not None:
            out.append((cmd1, None))
        else:
            out.append((cmd2, int(arg2)))

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
