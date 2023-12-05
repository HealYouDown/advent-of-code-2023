from utils import get_input
from dataclasses import dataclass
from itertools import chain
from functools import cache
import sys


@dataclass(frozen=True)
class Range:
    destination_range_start: int
    source_range_start: int
    range_length: int

    @classmethod
    def from_line(cls, line: str):
        nums = [int(j) for j in line.split(" ") if j]
        return cls(
            destination_range_start=nums[0],
            source_range_start=nums[1],
            range_length=nums[2],
        )

    @cache
    def check_in_source_range(self, value: int) -> bool:
        return value >= self.source_range_start and value < (
            self.source_range_start + self.range_length
        )

    @cache
    def calculate_destination(self, value: int) -> int:
        offset = value - self.source_range_start
        return self.destination_range_start + offset


@dataclass(frozen=True)
class Map:
    ranges: tuple[Range, ...]

    @classmethod
    def from_section(cls, section: str):
        ranges = []
        for line in section.splitlines()[1:]:
            ranges.append(Range.from_line(line))

        return cls(ranges=tuple(ranges))

    @cache
    def convert(self, value: int) -> int:
        for range_ in self.ranges:
            if range_.check_in_source_range(value):
                return range_.calculate_destination(value)

        return value


@dataclass(frozen=True)
class Almanac:
    seeds: tuple[int]
    seed_to_soil_map: Map
    soil_to_fertilizer_map: Map
    fertilizer_to_water_map: Map
    water_to_light_map: Map
    light_to_temperature_map: Map
    temperature_to_humidity_map: Map
    humidity_to_location_map: Map

    @classmethod
    def from_input(cls, text: str) -> None:
        (
            seeds_section,
            seed_to_soil_section,
            soil_to_fertilizer_section,
            fertilizer_to_water_section,
            water_to_light_section,
            light_to_temperature_section,
            temperature_to_humidity_section,
            humidity_to_location_section,
        ) = text.split("\n\n")

        seeds = [int(j) for j in seeds_section.split(": ")[1].split(" ") if j]

        return cls(
            seeds=seeds,
            seed_to_soil_map=Map.from_section(seed_to_soil_section),
            soil_to_fertilizer_map=Map.from_section(soil_to_fertilizer_section),
            fertilizer_to_water_map=Map.from_section(fertilizer_to_water_section),
            water_to_light_map=Map.from_section(water_to_light_section),
            light_to_temperature_map=Map.from_section(light_to_temperature_section),
            temperature_to_humidity_map=Map.from_section(
                temperature_to_humidity_section
            ),
            humidity_to_location_map=Map.from_section(humidity_to_location_section),
        )


def puzzle_1(almanac: Almanac) -> int:
    min_ = sys.maxsize

    for seed in almanac.seeds:
        soil = almanac.seed_to_soil_map.convert(seed)
        fertilizer = almanac.soil_to_fertilizer_map.convert(soil)
        water = almanac.fertilizer_to_water_map.convert(fertilizer)
        light = almanac.water_to_light_map.convert(water)
        temperature = almanac.light_to_temperature_map.convert(light)
        humidity = almanac.temperature_to_humidity_map.convert(temperature)
        location = almanac.humidity_to_location_map.convert(humidity)

        if location < min_:
            min_ = location

    return min_


def puzzle_2(almanac: Almanac) -> int:
    min_ = sys.maxsize

    seed_pairs = list(zip(almanac.seeds[::2], almanac.seeds[1::2]))
    seed_iterable = chain.from_iterable(
        range(pair[0], pair[0] + pair[1] + 1) for pair in seed_pairs
    )

    # FIXME: too many iterations
    for seed in seed_iterable:
        soil = almanac.seed_to_soil_map.convert(seed)
        fertilizer = almanac.soil_to_fertilizer_map.convert(soil)
        water = almanac.fertilizer_to_water_map.convert(fertilizer)
        light = almanac.water_to_light_map.convert(water)
        temperature = almanac.light_to_temperature_map.convert(light)
        humidity = almanac.temperature_to_humidity_map.convert(temperature)
        location = almanac.humidity_to_location_map.convert(humidity)

        if location < min_:
            min_ = location

    return min_


if __name__ == "__main__":
    almanac = Almanac.from_input(get_input(5))
    print(puzzle_1(almanac))
    # print(puzzle_2(almanac))
