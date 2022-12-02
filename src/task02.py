import re

from pathlib import Path
from contextlib import suppress

from PATHS import TEST_INPUT_DIR, TASK_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = TASK_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}.txt")


# SOLUTION

ENEMY_MOVES = {
    "A": "ROCK",
    "B": "PAPER",
    "C": "SCISSORS",
}

PLAYER_MOVES = {
    "X": "ROCK",
    "Y": "PAPER",
    "Z": "SCISSORS",
}

SCORES = {
    "ROCK": 1,
    "PAPER": 2,
    "SCISSORS": 3,
    # LOSS: 0,
    # DRAW: 3,
    # WIN: 6,
}


def _eval_move_score_part_one(move):
    enemy_move, player_move = move

    enemy_move = ENEMY_MOVES[enemy_move]
    player_move = PLAYER_MOVES[player_move]

    shape_score = SCORES[player_move]

    if SCORES[player_move] == SCORES[enemy_move]:
        result_score = 3

    elif (
        SCORES[player_move] == SCORES[enemy_move] + 1
        or SCORES[player_move] == SCORES[enemy_move] - 2
    ):
        result_score = 6

    else:
        result_score = 0

    return shape_score + result_score


def _eval_move_score_part_two(move):
    enemy_move, player_move = move

    enemy_move = ENEMY_MOVES[enemy_move]
    enemy_score = SCORES[enemy_move]

    if player_move == "X":
        score = enemy_score - 1

        if score == 0:
            score = 3

        return score

    elif player_move == "Y":
        return enemy_score + 3

    elif player_move == "Z":
        score = enemy_score + 1

        if score == 4:
            score = 1

        return score + 6

    return 0


# TASK-SPECIFIC BOILERPLATE


def solve_part_one(data):
    return sum(map(_eval_move_score_part_one, data))


def solve_part_two(data):
    return sum(map(_eval_move_score_part_two, data))


def solve_test(data):
    with suppress(NotImplementedError):
        print(f"Part 1 - {solve_part_one(data)}")

        print("-" * 15)

        print(f"Part 2 - {solve_part_two(data)}")


def solve(data):
    with suppress(NotImplementedError):
        print(f"Part 1 - {solve_part_one(data)}")

        print("-" * 15)

        print(f"Part 2 - {solve_part_two(data)}")


# GENERAL BOILERPLATE


def read_input(test: bool = False):
    path = TEST_INPUT_FILE if test else INPUT_FILE

    with open(path, "r") as file:
        content = file.read()

    return content.split("\n")


def parse_input(data):
    out = []

    pattern = re.compile(r"([A-C]) ([X-Z])")

    for line in data:
        result = pattern.match(line).groups()

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
    main(False)
