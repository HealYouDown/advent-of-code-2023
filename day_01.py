from utils import get_input
import re

NUMBERS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def puzzle_1(lines: list[str]):
    pattern_string = "|".join(n for n in NUMBERS.values())
    pattern = re.compile(pattern_string)
    matches = [re.findall(pattern, lines) for lines in lines]
    return sum(int(match[0] + match[-1]) for match in matches)


def puzzle_2(lines: list[str]):
    # re does not work because of overlapping strings, e.g. twone = two and one
    # pattern_string = "|".join([str(n) for n in NUMBERS.values()] + list(NUMBERS.keys()))
    # pattern = re.compile(f"{pattern_string}")
    patterns_to_find = [str(n) for n in NUMBERS.values()] + list(NUMBERS.keys())

    sum = 0
    for line in lines:
        # matches = re.findall(pattern, line)
        # runs very fast x)
        matches = []
        for i in range(len(line)):
            for pattern in patterns_to_find:
                if line[i:].startswith(pattern):
                    matches.append(pattern)

        start: str = matches[0]
        end: str = matches[-1]
        if not start.isdigit():
            start = NUMBERS[start]
        if not end.isdigit():
            end = NUMBERS[end]

        sum += int(start + end)

    return sum


if __name__ == "__main__":
    lines = [row.strip() for row in get_input(1).splitlines()]
    print(puzzle_1(lines))
    print(puzzle_2(lines))
