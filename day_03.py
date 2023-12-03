from utils import get_input
from dataclasses import dataclass
import re
from collections import defaultdict


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def __eq__(self, other: "Pos") -> bool:
        return self.x == other.x and self.y == other.y


@dataclass(frozen=True)
class PartNumber:
    value: int
    start_pos: Pos
    end_pos: Pos

    def get_surrounding_positions(self) -> set[Pos]:
        surrounding_positions: set[Pos] = set()
        surrounding_positions.update(
            [
                Pos(x=x, y=self.start_pos.y - 1)
                for x in range(self.start_pos.x - 1, self.end_pos.x + 2)
            ]
        )
        surrounding_positions.update(
            [
                Pos(x=x, y=self.start_pos.y + 1)
                for x in range(self.start_pos.x - 1, self.end_pos.x + 2)
            ]
        )
        surrounding_positions.add(Pos(x=self.start_pos.x - 1, y=self.start_pos.y))
        surrounding_positions.add(Pos(x=self.end_pos.x + 1, y=self.start_pos.y))

        return surrounding_positions


@dataclass(frozen=True)
class Symbol:
    pos: Pos
    symbol: str


def puzzle_1(part_numbers: list[PartNumber], symbols: list[Symbol]):
    sum = 0
    for part_number in part_numbers:
        if any(
            symbol.pos in part_number.get_surrounding_positions() for symbol in symbols
        ):
            sum += part_number.value

    return sum


def puzzle_2(part_numbers: list[PartNumber], symbols: list[Symbol]):
    gear_symbols = list(filter(lambda s: s.symbol == "*", symbols))
    gears_to_matching_part_nums: dict[Symbol, list[PartNumber]] = defaultdict(list)

    for part_number in part_numbers:
        surrounding_positions = part_number.get_surrounding_positions()
        for symbol in gear_symbols:
            if symbol.pos in surrounding_positions:
                gears_to_matching_part_nums[symbol].append(part_number)

    sum = 0
    for matching_part_numbers in gears_to_matching_part_nums.values():
        if len(matching_part_numbers) == 2:
            sum += matching_part_numbers[0].value * matching_part_numbers[1].value

    return sum


if __name__ == "__main__":
    symbols: list[Symbol] = []
    part_numbers: list[PartNumber] = []

    pattern = re.compile(r"(\d+)|([^.])")
    for row, line in enumerate(get_input(3).splitlines()):
        for match in pattern.finditer(line):
            value = match.group()
            if value.isdigit():
                part_numbers.append(
                    PartNumber(
                        value=int(value),
                        start_pos=Pos(x=match.start(), y=row),
                        end_pos=Pos(x=match.end() - 1, y=row),
                    )
                )
            else:
                symbols.append(Symbol(symbol=value, pos=Pos(x=match.start(), y=row)))

    # print(puzzle_1(part_numbers, symbols))
    print(puzzle_2(part_numbers, symbols))
