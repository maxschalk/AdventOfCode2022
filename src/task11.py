import re

from operator import add, mul
from dataclasses import dataclass
from collections import deque
from pathlib import Path
from contextlib import suppress

from PATHS import TEST_INPUT_DIR, TASK_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = TASK_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")


# SOLUTION


@dataclass
class Monkey:
    number: int
    items: deque[int]
    worry_func: callable
    test_divisible_by: int
    test_true_monkey_number: int
    test_false_monkey_number: int

    items_inspected: int = 0

    def reduce_worry(self, item):
        return item % (19 * 3 * 13 * 7 * 5 * 11 * 17 * 2)
        return item // 3

    def throw_next_item(self) -> tuple[int, int]:
        item = self.items.popleft()

        item = self.worry_func(item)

        item = self.reduce_worry(item)

        test_result = item % self.test_divisible_by == 0

        target_monkey = (
            self.test_true_monkey_number
            if test_result
            else self.test_false_monkey_number
        )

        self.items_inspected += 1

        return (item, target_monkey)

    def throw_all_items(self) -> tuple[tuple[int, int]]:
        return tuple(self.throw_next_item() for _ in range(len(self.items)))


def _solve_part_one(monkeys: list[Monkey]):

    for _ in range(20):
        for monkey in monkeys:
            throws = monkey.throw_all_items()

            for item, target_monkey in throws:
                monkeys[target_monkey].items.append(item)

    inspections = sorted(map(lambda m: m.items_inspected, monkeys))

    return inspections[-1] * inspections[-2]


def _solve_part_two(monkeys):
    for _ in range(10000):
        for monkey in monkeys:
            throws = monkey.throw_all_items()

            for item, target_monkey in throws:
                monkeys[target_monkey].items.append(item)

    inspections = sorted(map(lambda m: m.items_inspected, monkeys))

    return inspections[-1] * inspections[-2]


# TASK-SPECIFIC BOILERPLATE


def solve_part_one(monkeys):
    print(_solve_part_one(monkeys))


def solve_part_two(monkeys):
    print(_solve_part_two(monkeys))


def solve_test(monkeys):
    with suppress(NotImplementedError):
        print(f"Part 1 - {_solve_part_one(monkeys)}")

        print("-" * 15)

        print(f"Part 2 - {_solve_part_two(monkeys)}")


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


def worry_func_factory(op, arg):
    op = {"+": add, "*": mul}[op]

    if arg == "old":

        def worry_func(old):
            return op(old, old)

    else:

        def worry_func(old):
            return op(old, int(arg))

    return worry_func


def parse_input(data):
    data = tuple(map(str.strip, data))

    monkeys = []

    for i in range(0, len(data), 7):
        chunk = iter(data[i : i + 6])

        monkey_number = re.match(r"Monkey (\d+):", next(chunk)).groups()[0]

        items = deque(map(int, re.findall(r"(\d+)", next(chunk))))

        op, arg = re.match(
            r"Operation: new = old (\+|\*) (old|\d+)", next(chunk)
        ).groups()
        worry_func = worry_func_factory(op, arg)

        test_divisible_by = int(
            re.match(r"Test: divisible by (\d+)", next(chunk)).groups()[0]
        )

        test_true_monkey_number = int(
            re.match(r"If true: throw to monkey (\d+)", next(chunk)).groups()[0]
        )

        test_false_monkey_number = int(
            re.match(r"If false: throw to monkey (\d+)", next(chunk)).groups()[0]
        )

        monkey = Monkey(
            number=monkey_number,
            items=items,
            worry_func=worry_func,
            test_divisible_by=test_divisible_by,
            test_true_monkey_number=test_true_monkey_number,
            test_false_monkey_number=test_false_monkey_number,
        )

        monkeys.append(monkey)

    return monkeys


def main(test=False):
    data = read_input(test)
    data = parse_input(data)

    if test:
        solve_test(data)
    else:
        solve(data)


if __name__ == "__main__":
    main(test=False)
