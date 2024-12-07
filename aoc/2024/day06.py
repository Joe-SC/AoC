# %%
"""https://adventofcode.com/2024/day/6"""

from aoc_utils import fetch_input_data
import logging
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
import re
import time
from IPython.display import clear_output

logger = logging.getLogger(__name__)
actual_input = fetch_input_data(2024, 6)

sample_input = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...\
"""

def parse_input(inputs: str) -> list[list[str]]:
    return [[c for c in row] for row in inputs.splitlines()]

def find_guard(grid: list[list[str]], target: str="v^<>") -> tuple[int, int]:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in target:
                return (x, y), cell

def is_in_grid(grid: list[list[str]], pos: tuple[int, int]) -> bool:
    x, y = pos
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])

def is_obstructed(grid: list[list[str]], pos: tuple[int, int], direction: str) -> bool:
    x, y = pos
    if direction == '^':
        return grid[y-1][x] == '#'
    elif direction == 'v':
        return grid[y+1][x]== '#'
    elif direction == '>':
        return grid[y][x+1] == '#'
    elif direction == '<':
        return grid[y][x-1] == '#'
    
def walk_forward(grid: list[list[str]], pos: tuple[int, int], direction: str) -> tuple[int, int]:
    x, y = pos
    if direction == '^':
        x_new, y_new = x, y-1
        grid[y_new][x_new] = '^'
        grid[y][x] = 'X'
    elif direction == 'v':
        x_new, y_new = x, y+1
        grid[y_new][x_new] = 'v'
        grid[y][x] = 'X'
    elif direction == '>':
        x_new, y_new = x+1, y
        grid[y_new][x_new] = '>'
        grid[y][x] = 'X'
    elif direction == '<':
        x_new, y_new = x-1, y
        grid[y_new][x_new] = '<'
        grid[y][x] = 'X'
    return grid, (x_new, y_new)

def turn_right(grid: list[list[str]], pos: str, direction: str) -> str:
    x, y = pos
    if direction == '^':
        new_direction = '>'
    elif direction == 'v':
        new_direction = '<'
    elif direction == '>':
        new_direction = 'v'
    elif direction == '<':
        new_direction = '^'
    grid[y][x] = new_direction
    return grid, new_direction

def grid_to_str(grid: list[list[str]]) -> str:
    return '\n'.join([''.join(row) for row in grid])

def about_to_leave(grid: list[list[str]], pos: tuple[int, int], direction: str) -> bool:
    x, y = pos
    if direction == '^':
        return y == 0  # Would step outside top
    elif direction == 'v':
        return y == len(grid) - 1  # Would step outside bottom
    elif direction == '>':
        return x == len(grid[0]) - 1  # Would step outside right
    elif direction == '<':
        return x == 0  # Would step outside left
    
def count_char(grid: list[list[str]], char='X') -> int:
    return sum(row.count(char) for row in grid)

def walk_grid(grid: list[list[str]], show:bool=False, sleep:float=0.1) -> list[list[str]]:

    def show_grid(grid=grid, sleep_for=0.2) -> None:
        #flush stdout
        clear_output(wait=True)
        #wait a second
        time.sleep(sleep_for)
        print(grid_to_str(grid))

    pos, direction = find_guard(grid)
    while is_in_grid(grid, pos):
        if about_to_leave(grid, pos, direction):
            # leave the grid
            grid[pos[1]][pos[0]] = 'X'
            # exit loop
            break
        
        while is_obstructed(grid, pos, direction):
            grid, direction = turn_right(grid, pos, direction)
        grid, pos = walk_forward(grid, pos, direction)
        if show: show_grid(grid, sleep_for=sleep)
    if show: show_grid(grid)
    return grid


def detect_loop(grid: list[list[str]], show: bool = False) -> bool:
    pos, direction = find_guard(grid)
    start_pos = pos
    visited_states = set()  # Track (position, direction) states
    steps = 0
    max_steps = len(grid) * len(grid[0]) * 4  # Maximum possible unique states
    
    while is_in_grid(grid, pos):
        steps += 1
        if steps > max_steps:
            print(f"Warning: Maximum steps {max_steps} exceeded at position {pos}")
            return False
            
        if about_to_leave(grid, pos, direction):
            return False
            
        state = (pos, direction)
        if state in visited_states:
            return True
        visited_states.add(state)
        
        original_direction = direction
        turns = 0
        while is_obstructed(grid, pos, direction):
            grid, direction = turn_right(grid, pos, direction)
            turns += 1
            if turns > 4:  # Full rotation without finding unobstructed direction
                print(f"Warning: Stuck at position {pos}")
                return False
                
        grid, pos = walk_forward(grid, pos, direction)
    
    return False

def find_loop_positions(grid: list[list[str]]) -> int:
    start_pos, _ = find_guard(grid)
    loop_positions = []
    total_positions = sum(row.count('.') for row in grid) - 1  # Excluding guard position
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '.' and (x, y) != start_pos:
                # Test this position
                test_grid = [row[:] for row in grid]
                test_grid[y][x] = '#'
                if detect_loop(test_grid):
                    loop_positions.append((x, y))
                if len(loop_positions) % 10 == 0:
                    print(f"Tested {x},{y}. Found {len(loop_positions)} loop positions")
    
    return len(loop_positions)


if __name__ == "__main__":

    # Part 1
    sample_grid = parse_input(sample_input)
    final_grid = walk_grid(sample_grid, show=True, sleep=0)
    assert count_char(final_grid, char='X') == 41
    assert grid_to_str(final_grid) == """\
    ....#.....
    ....XXXXX#
    ....X...X.
    ..#.X...X.
    ..XXXXX#X.
    ..X.X.X.X.
    .#XXXXXXX.
    .XXXXXXX#.
    #XXXXXXX..
    ......#X..\
    """
    del final_grid

    grid = parse_input(actual_input)
    final_grid = walk_grid(grid)
    print("Part 1:", count_char(final_grid, char='X'))

    # Part 2
    sample_grid = parse_input(sample_input)
    assert find_loop_positions(sample_grid) == 6

    grid = parse_input(actual_input)
    result = find_loop_positions(grid)
    print(f"Part 2 solution: {result}")