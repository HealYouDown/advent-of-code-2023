from utils import get_input
from dataclasses import dataclass
from collections import deque
from functools import cache


@dataclass(frozen=True)
class Scratchcard:
    idx: int
    winning_numbers: tuple[int]
    owning_numbers: tuple[int]

    @classmethod
    def from_line(cls, idx: int, line: str):
        _, num_part = line.split(": ")
        wn_part, on_part = num_part.split("|")
        wn_numbers = tuple(int(j) for j in wn_part.strip().split(" ") if j)
        on_numbers = tuple(int(j) for j in on_part.strip().split(" ") if j)

        return cls(idx=idx, winning_numbers=wn_numbers, owning_numbers=on_numbers)

    @cache  # mvp carry
    def calculate_winning_cards_count(self) -> int:
        count = 0
        for num in set(self.owning_numbers):
            if num in self.winning_numbers:
                count += self.owning_numbers.count(num)

        return count

    def calculate_score(self) -> int:
        winning_count = self.calculate_winning_cards_count()
        if winning_count == 0:
            return 0

        return 2 ** (winning_count - 1)


def puzzle_1(scratchcards: list[Scratchcard]) -> int:
    return sum(scratchcard.calculate_score() for scratchcard in scratchcards)


def puzzle_2(scratchcards: list[Scratchcard]) -> int:
    processing = deque(scratchcards)
    count = len(scratchcards)
    # not quite the fastest, but it works x)
    # better approch would probably be to cache the result for the whole chain deep down
    # no idea tho
    while processing:
        current_card = processing.popleft()
        winning_cards_count = current_card.calculate_winning_cards_count()
        new_cards = scratchcards[
            current_card.idx + 1 : current_card.idx + winning_cards_count + 1
        ]
        count += len(new_cards)
        processing.extend(new_cards)

    return count


if __name__ == "__main__":
    scratchcards = [
        Scratchcard.from_line(idx, line)
        for idx, line in enumerate(get_input(4).splitlines())
    ]

    print(puzzle_1(scratchcards))
    print(puzzle_2(scratchcards))
