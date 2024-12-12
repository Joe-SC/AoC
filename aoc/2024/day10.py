"""https://adventofcode.com/2024/day/10"""

from aoc_utils import fetch_input_data
import logging
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
from itertools import product
import copy
import math

logger = logging.getLogger(__name__)
actual_input = fetch_input_data(2024, 8)

def convert_to_grid(inputs: str, astype:str = 'str') -> list[list[int]]:
    if astype == 'int':
        return [[int(c) for c in row] for row in inputs.splitlines()]
    elif astype == 'str':
        return [[c for c in row] for row in inputs.splitlines()]

def grid_to_str(grid: list[list[str]]) -> str:
    return '\n'.join([''.join(row) for row in grid])

def find_trailheads(grid: list[list[str]], target: str | int=0) -> list[tuple[int, int]]:
    trailheads = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == target:
                trailheads.append((x, y))
    return trailheads

def search_neighbors_for(grid: list[list[str]], pos: tuple[int, int], target: str) -> list[tuple[int, int]]:
    x, y = pos
    neighbors = []
    for dx, dy in product([-1, 0, 1], repeat=2):
        if dx == dy == 0:
            continue
        x_new, y_new = x + dx, y + dy
        if 0 <= y_new < len(grid) and 0 <= x_new < len(grid[0]) and grid[y_new][x_new] == target:
            neighbors.append((x_new, y_new))
    return neighbors