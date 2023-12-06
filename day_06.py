from utils import get_input
from dataclasses import dataclass


@dataclass(frozen=True)
class Race:
    time: int
    record: int

    def beats_record(self, t: int) -> bool:
        # distance < (time - holding) * holding
        # e.g. 9 < (7 - x) * x | for 0 <= x <= time
        return self.record < ((self.time - t) * t)

    def calculate_num_winning_times(self) -> int:
        first_winning_number: int = None
        last_winning_number: int = None

        for t in range(0, self.time + 1):
            if self.beats_record(t):
                first_winning_number = t
                break

        for t in range(self.time, 0, -1):
            if self.beats_record(t):
                last_winning_number = t
                break

        return (last_winning_number - first_winning_number) + 1


def puzzle_1(races: list[Race]):
    res = 1
    for race in races:
        res *= race.calculate_num_winning_times()
    return res


def puzzle_2(race: Race):
    return race.calculate_num_winning_times()


if __name__ == "__main__":
    times_line, distances_line = get_input(6).splitlines()
    times = [int(i) for i in times_line.split(": ")[1].split(" ") if i]
    distances = [int(i) for i in distances_line.split(": ")[1].split(" ") if i]

    races_part1 = [Race(t, d) for t, d in zip(times, distances)]
    race_part_2 = Race(
        int("".join(str(i) for i in times)),
        int("".join(str(i) for i in distances)),
    )

    print(puzzle_1(races_part1))
    print(puzzle_2(race_part_2))
