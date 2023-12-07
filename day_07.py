from utils import get_input
from dataclasses import dataclass
import enum
from collections import Counter
from itertools import product


class HandType(enum.IntEnum):
    NOTHING = enum.auto()
    ONE_PAIR = enum.auto()
    TWO_PAIR = enum.auto()
    THREE = enum.auto()
    FULL_HOUSE = enum.auto()
    FOUR = enum.auto()
    FIVE = enum.auto()


@dataclass(frozen=True)
class Card:
    symbol: str

    def __repr__(self) -> str:
        return repr(self.symbol)

    @property
    def value(self) -> int:
        if self.symbol.isdigit():
            return int(self.symbol)

        return {
            "T": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14,
        }[self.symbol]

    def __eq__(self, other: "Card") -> bool:
        return self.value == other.value

    def __lt__(self, other: "Card") -> bool:
        return self.value < other.value


@dataclass(frozen=True)
class JokerCard(Card):
    @property
    def value(self) -> int:
        return 1


@dataclass(frozen=True)
class Hand:
    cards: list[Card]
    bid: int

    @classmethod
    def from_line(cls, line: str, joker_cards: bool = False):
        cards_inp, bid = line.split(" ")

        cards: list[Card] = []
        for symbol in cards_inp:
            if symbol == "J" and joker_cards:
                card = JokerCard(symbol)
            else:
                card = Card(symbol)

            cards.append(card)

        return cls(
            cards=cards,
            bid=int(bid),
        )

    @property
    def card_values(self) -> tuple[int, int, int, int, int]:
        return tuple(card.value for card in self.cards)

    def _calculate_hand_type_without_joker(self) -> HandType:
        counter = Counter(self.cards)

        is_five = len(counter) == 1
        if is_five:
            return HandType.FIVE

        is_four = any(v == 4 for v in counter.values())
        if is_four:
            return HandType.FOUR

        is_full_house = len(counter) == 2
        if is_full_house:
            return HandType.FULL_HOUSE

        is_three = any(v == 3 for v in counter.values())
        if is_three:
            return HandType.THREE

        pairs_count = len([True for v in counter.values() if v == 2])
        is_two_pairs = pairs_count == 2
        if is_two_pairs:
            return HandType.TWO_PAIR

        is_one_pair = pairs_count == 1
        if is_one_pair:
            return HandType.ONE_PAIR

        return HandType.NOTHING

    def _calculate_best_hand_type_using_jokers(self) -> HandType:
        if not any(c.symbol == "J" for c in self.cards):
            return self._calculate_hand_type_without_joker()

        # bruteforcing the best combo by creating permutations for replacing each J card
        # with a card of another already included symbol
        unique_symbols = set(card.symbol for card in self.cards if card.symbol != "J")
        if not unique_symbols:  # all 5 cards are jokers
            return HandType.FIVE

        joker_indicies = tuple(
            i for i, card in enumerate(self.cards) if card.symbol == "J"
        )
        perms = tuple(product(unique_symbols, repeat=len(joker_indicies)))

        possible_hand_types: set[HandType] = set()
        for perm in perms:
            cards = self.cards[:]
            for i, joker_idx in enumerate(joker_indicies):
                cards[joker_idx] = Card(symbol=perm[i])
            joker_hand = Hand(cards=cards, bid=0)
            possible_hand_types.add(joker_hand._calculate_hand_type_without_joker())

        return max(possible_hand_types)

    def calculate_hand_type(self, with_joker_rules: bool) -> HandType:
        if with_joker_rules:
            return self._calculate_best_hand_type_using_jokers()
        return self._calculate_hand_type_without_joker()


def puzzle_1() -> int:
    hands = [Hand.from_line(line) for line in get_input(7).splitlines()]
    sorted_hands = sorted(
        hands,
        key=lambda hand: (
            hand.calculate_hand_type(with_joker_rules=False),
            *hand.card_values,
        ),
    )
    return sum(rank * hand.bid for rank, hand in enumerate(sorted_hands, start=1))


def puzzle_2() -> int:
    hands = [
        Hand.from_line(line, joker_cards=True) for line in get_input(7).splitlines()
    ]
    sorted_hands = sorted(
        hands,
        key=lambda h: (
            h.calculate_hand_type(with_joker_rules=True),
            *h.card_values,
        ),
    )
    return sum(rank * hand.bid for rank, hand in enumerate(sorted_hands, start=1))


if __name__ == "__main__":
    print(puzzle_1())
    print(puzzle_2())
