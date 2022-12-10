from __future__ import annotations

import re

from enum import Enum
from dataclasses import dataclass

from pathlib import Path
from contextlib import suppress

from PATHS import TEST_INPUT_DIR, TASK_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = TASK_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")


# SOLUTION


class CommandType(Enum):
    cd = "cd"
    ls = "ls"


@dataclass
class Command:
    command_type: CommandType

    argument: str | None = None


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory(File):
    children: dict[str, File | Directory]


def parse_to_file_tree(data):
    current_path = []
    root = Directory(name="/", size=0, children=dict())

    for line in data:
        if isinstance(line, Command):
            if line.command_type == CommandType.ls:
                pass

            elif line.command_type == CommandType.cd:
                destination_name = line.argument

                if destination_name == "..":
                    current_path.pop()

                elif destination_name == root.name:
                    current_path = [root]

                else:
                    destination = current_path[-1].children.get(
                        destination_name,
                        Directory(name=destination_name, size=0, children=dict()),
                    )
                    current_path[-1].children[destination_name] = destination
                    current_path.append(destination)

        elif isinstance(line, File):
            current_path[-1].children[line.name] = line

    return root


def calculate_file_tree_sizes(root_node):
    if type(root_node) == File:
        return root_node.size

    for child in root_node.children.values():
        calculate_file_tree_sizes(child)

    root_node.size = sum(map(lambda c: c.size, root_node.children.values()))


def sum_filtered_sizes(root_node, predicate):
    result = 0

    if predicate(root_node):
        result += root_node.size

    if type(root_node) == Directory:
        result += sum(
            map(lambda c: sum_filtered_sizes(c, predicate), root_node.children.values())
        )

    return result


def _solve_part_one(data):
    file_tree_root = parse_to_file_tree(data)

    calculate_file_tree_sizes(file_tree_root)

    predicate = lambda node: type(node) == Directory and node.size <= 100000
    return sum_filtered_sizes(file_tree_root, predicate)


def get_nodes(root_node, predicate, accumulator):
    if predicate(root_node):
        accumulator.append(root_node)

    if type(root_node) == Directory:
        for child in root_node.children.values():
            get_nodes(child, predicate, accumulator)

    return accumulator


def _solve_part_two(data):
    FILESYSTEM_SPACE = 70000000
    NEEDED_SPACE = 30000000

    file_tree_root = parse_to_file_tree(data)

    calculate_file_tree_sizes(file_tree_root)

    to_delete = NEEDED_SPACE - (FILESYSTEM_SPACE - file_tree_root.size)

    predicate = lambda node: type(node) == Directory and node.size >= to_delete
    relevant_directories = get_nodes(file_tree_root, predicate, [])

    return sorted(map(lambda d: d.size, relevant_directories))[0]


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
    pattern_cd_command = re.compile(r"\$ (cd) (.+)")
    pattern_ls_command = re.compile(r"\$ (ls)")
    pattern_dir = re.compile(r"dir (.+)")
    pattern_file = re.compile(r"(\d+) (.+)")

    out = []
    for line in data:

        if parsed := getattr(pattern_cd_command.match(line), "groups", lambda: False)():
            cmd, arg = parsed

            result = Command(command_type=CommandType[cmd], argument=arg)

        elif parsed := getattr(
            pattern_ls_command.match(line), "groups", lambda: False
        )():
            cmd = parsed[0]
            result = Command(command_type=CommandType[cmd])

        elif parsed := getattr(pattern_dir.match(line), "groups", lambda: False)():
            name = parsed[0]

            result = Directory(name=name, size=0, children=dict())

        elif parsed := getattr(pattern_file.match(line), "groups", lambda: False)():
            size, name = parsed

            result = File(name=name, size=int(size))

        else:
            print("This should not happen")
            exit(1)

        out.append(result)

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
