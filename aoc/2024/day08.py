%load_ext autoreload
%autoreload 2
"""https://adventofcode.com/2024/day/8"""

from aoc_utils import fetch_input_data
import logging
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
from itertools import product
import copy

logger = logging.getLogger(__name__)
actual_input = fetch_input_data(2024, 8)
sample_input = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............\
"""

# sample_input = """\
# ..........
# ..........
# ..........
# ....a.....
# ..........
# .....a....
# ..........
# ..........
# ..........
# ..........\
# """

# sample_input = """\
# T.........
# ...T......
# .T........
# ..........
# ..........
# ..........
# ..........
# ..........
# ..........
# ..........\
# """



def convert_to_grid(inputs: str) -> list[list[str]]:
    return [[c for c in row] for row in inputs.splitlines()]

def grid_shape(grid: list[list[str]]) -> tuple[int, int]:
    return len(grid[0]), len(grid)

def grid_to_str(grid: list[list[str]]) -> str:
    return '\n'.join([''.join(row) for row in grid])

def search_antennas(grid: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
    x_max, y_max = grid_shape(grid)
    antennas = {}
    for x, y in product(range(x_max), range(y_max)):
        char = grid[y][x]
        if char != '.':
            if char not in antennas.keys():
                antennas[char] = []
            # logger.debug(f"Found {char} at {x}, {y}")
            antennas[char].append((x, y))
    return antennas

def distance(loc1: tuple[int, int], loc2: tuple[int, int]) -> int:
    return loc1[0] - loc2[0], loc1[1] - loc2[1]

def part_1_antinode_grid(grid: list[list[str]]) -> list[list[str]]:
    x_max, y_max = grid_shape(grid)
    antinode_grid = copy.deepcopy(grid)
    antinode_locations = set()
    antenna_locations = search_antennas(grid)

    for frequency, locations in antenna_locations.items():
        for a1, a2 in product(locations, locations):
            if a1 != a2:
                dx, dy = distance(a1, a2)
                an_x, an_y = a1[0] + dx, a1[1] + dy
                is_out_of_bounds = (
                    an_x < 0 or 
                    an_x >= x_max or 
                    an_y < 0 or 
                    an_y >= y_max
                )
                if is_out_of_bounds:
                    continue
                antinode_grid[an_y][an_x] = '#'
                antinode_locations.add((an_x, an_y))
    return antinode_grid, antinode_locations

if __name__=="__main__":
    sample_grid = convert_to_grid(sample_input)
    sample_antinode_grid, sample_antinode_locations = part_1_antinode_grid(sample_grid)
    assert len(sample_antinode_locations) == 14
    part_1_grid = convert_to_grid(actual_input)
    part_1_antinode_grid, part_1_antinode_locations = part_1_antinode_grid(part_1_grid)
    print('Part 1:',len(part_1_antinode_locations))