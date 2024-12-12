"""https://adventofcode.com/2024/day/8"""

from aoc_utils import fetch_input_data
import logging
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
from itertools import product
import copy
import math

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

test_input = """\
T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........\
"""

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
                    an_x < 0 or an_x >= x_max or 
                    an_y < 0 or an_y >= y_max
                )
                if is_out_of_bounds:
                    continue
                antinode_grid[an_y][an_x] = '#'
                antinode_locations.add((an_x, an_y))
    return antinode_grid, antinode_locations

def part_2_antinode_grid(grid: list[list[str]]) -> list[list[str]]:
    x_max, y_max = grid_shape(grid)
    antinode_grid = copy.deepcopy(grid)
    antinode_locations = set()
    antenna_locations = search_antennas(grid)

    for frequency, locations in antenna_locations.items():
        for a1, a2 in product(locations, locations):
<<<<<<< HEAD
            if a1 != a2:
                dx, dy = distance(a1, a2)
                multiplier = 1
                is_out_of_bounds = False
                while not is_out_of_bounds:
                    an_x, an_y = a1[0] + (dx * multiplier), a1[1] + (dy * multiplier)
                    is_out_of_bounds = (
                        an_x < 0 or 
                        an_x >= x_max or 
                        an_y < 0 or 
                        an_y >= y_max
                    )
                    if is_out_of_bounds:
                        break
                    antinode_grid[an_y][an_x] = '#'
                    antinode_locations.add((an_x, an_y))
                    multiplier += 1
=======
            if a1 == a2:
                continue
                
            dx, dy = distance(a2, a1)
            if dx != 0 and dy != 0:
                gcd = abs(math.gcd(dx, dy))
                dx = dx // gcd
                dy = dy // gcd
            elif dx != 0:
                dx = dx // abs(dx)
            elif dy != 0:
                dy = dy // abs(dy)
                
            for direction in [-1, 1]:
                curr_x, curr_y = a1[0], a1[1]
                while True:
                    curr_x += dx * direction
                    curr_y += dy * direction
                    
                    is_out_of_bounds = (
                        curr_x < 0 or curr_x >= x_max or 
                        curr_y < 0 or curr_y >= y_max
                        )
                    if is_out_of_bounds:
                        break
                    
                    antinode_grid[curr_y][curr_x] = '#'
                    antinode_locations.add((curr_x, curr_y))
                
>>>>>>> 9fd2e0a6752482ec9b84f54073b8864a333d58f9
    return antinode_grid, antinode_locations

if __name__=="__main__":
    sample_grid = convert_to_grid(sample_input)
    sample_antinode_grid, sample_antinode_locations = part_1_antinode_grid(sample_grid)
    assert len(sample_antinode_locations) == 14
    part_1_grid = convert_to_grid(actual_input)
    part_1_antinode_grid, part_1_antinode_locations = part_1_antinode_grid(part_1_grid)
    print('Part 1:',len(part_1_antinode_locations))

    test_grid=convert_to_grid(test_input)
    test_antinode_grid, test_antinode_locations = part_2_antinode_grid(test_grid)
    assert len(test_antinode_locations) == 9
    sample_grid = convert_to_grid(sample_input)
    sample_antinode_grid, sample_antinode_locations = part_2_antinode_grid(sample_grid)
    assert len(sample_antinode_locations) == 34
    grid = convert_to_grid(actual_input)
    antinode_grid, antinode_locations = part_2_antinode_grid(grid)
    print('Part 2:', len(part_1_antinode_locations))