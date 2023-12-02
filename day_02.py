from utils import get_input
from dataclasses import dataclass
from collections import defaultdict
import enum
from functools import reduce


class CubeColor(enum.IntEnum):
    RED = enum.auto()
    GREEN = enum.auto()
    BLUE = enum.auto()

    @classmethod
    def from_string(cls, color: str):
        return cls[color.upper()]


@dataclass
class Game:
    id: int
    sets: list[list[tuple[int, CubeColor]]]

    @classmethod
    def from_line(cls, line: str):
        id_part, games_part = line.split(":")
        id = int(id_part.split(" ")[-1])

        sets = []
        for set_string in games_part.split(";"):
            ball_picks = []
            for pick in set_string.split(","):
                amount_string, color_string = pick.strip().split(" ")
                amount = int(amount_string)
                color = CubeColor.from_string(color_string)
                ball_picks.append((amount, color))
            sets.append(ball_picks)

        return cls(id=id, sets=sets)


def puzzle_1(games: list[Game]):
    possible_games: list[Game] = []
    for game in games:
        max_cube_color_count: dict[CubeColor, int] = defaultdict(int)
        for set_ in game.sets:
            for amount, color in set_:
                if amount > max_cube_color_count[color]:
                    max_cube_color_count[color] = amount

        is_possible = (
            max_cube_color_count[CubeColor.RED] <= 12
            and max_cube_color_count[CubeColor.GREEN] <= 13
            and max_cube_color_count[CubeColor.BLUE] <= 14
        )
        if is_possible:
            possible_games.append(game)

    return sum(game.id for game in possible_games)


def puzzle_2(games: list[Game]):
    total_power = 0
    for game in games:
        max_cube_color_count: dict[CubeColor, int] = defaultdict(int)
        for set_ in game.sets:
            for amount, color in set_:
                if amount > max_cube_color_count[color]:
                    max_cube_color_count[color] = amount

        power = reduce(lambda x, y: x * y, max_cube_color_count.values())
        total_power += power
    return total_power


if __name__ == "__main__":
    games = [Game.from_line(line) for line in get_input(2).splitlines()]
    print(puzzle_1(games))
    print(puzzle_2(games))
