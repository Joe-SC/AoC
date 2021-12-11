import os

from itertools import product
from types import NoneType

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day11_input.txt")) as f:
    actual_input = f.read()

sample_input = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


@print_time_taken
def solve(inputs):
    octopi = {
        complex(x, y): int(level)
        for y, line in enumerate(inputs.splitlines())
        for x, level in enumerate(line)
    }
    directions = [complex(*d) for d in product((-1, 0, 1), repeat=2) if d != (0, 0)]
    neighbours = {
        xy: tuple(n for n in (xy + d for d in directions) if n in octopi)
        for xy in octopi
    }

    flashes, step = 0, 0
    while True:
        step += 1
        for xy in octopi:
            octopi[xy] += 1
        flashed = set()
        while True:
            flasher = next((xy for xy, level in octopi.items() if level > 9), None)
            if flasher is None:
                break
            octopi[flasher] = 0
            flashed.add(flasher)
            for neighbour in (n for n in neighbours[flasher] if n not in flashed):
                octopi[neighbour] += 1

        flashes += len(flashed)
        if step == 100:
            print(f"Part 1: {flashes}")
        if len(flashed) == 100:
            print(f"Part 2: {step}\n")
            break


solve(sample_input)
solve(actual_input)
