"""https://adventofcode.com/2018/day/10"""

import os
import re

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), "inputs/day10_input.txt")) as f:
    actual_input = f.read()

sample_input = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""


@print_time_taken
def solve(stars, letter_height):
    position, velocity = [], []
    for x, y, dx, dy in (map(int, re.findall(r"-?\d+", l)) for l in stars.splitlines()):
        position.append((x, y))
        velocity.append((dx, dy))

    elapsed_time = 0
    while True:
        elapsed_time += 1
        position = [(x + dx, y + dy) for (x, y), (dx, dy) in zip(position, velocity)]
        min_y, max_y = min(xy[1] for xy in position), max(xy[1] for xy in position)
        if max_y - min_y <= letter_height:
            break

    print(f"Part 1:")
    min_x, max_x = min(xy[0] for xy in position), max(xy[0] for xy in position)
    for y in range(min_y - 2, max_y + 3):
        for x in range(min_x - 2, max_x + 3):
            print("\u2588" if (x, y) in position else ".", end="")
        print()
    print(f"Part 2: {elapsed_time}\n")


solve(sample_input, 7)
solve(actual_input, 10)
