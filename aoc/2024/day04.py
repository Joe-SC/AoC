"""https://adventofcode.com/2024/day/4"""

from aoc_utils import fetch_input_data
import logging
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
import re

logger = logging.getLogger(__name__)
actual_input = fetch_input_data(2024, 4)

sample_input_1="""\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX\
"""

sample_input_2="""\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX\
"""


def convert_to_grid(inputs: str) -> list[list[str]]:
    return [[c for c in row] for row in inputs.splitlines()]


def solve_part_1(grid):
    """
    Find all occurrences of 'XMAS' in the grid in all 8 directions.
    Returns the total count of occurrences.
    """
    rows, cols = len(grid), len(grid[0])
    total = 0
    target = "XMAS"
    
    # Define all 8 directions to check
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
        (0, -1),  # left
        (-1, 0),  # up
        (-1, -1), # diagonal up-left
        (1, -1)   # diagonal down-left
    ]
    
    def check_direction(row, col, dx, dy):
        """Check if 'XMAS' exists starting from (row, col) in direction (dx, dy)"""
        if not (0 <= row + 3*dx < rows and 0 <= col + 3*dy < cols):
            return False
            
        return all(grid[row + i*dx][col + i*dy] == target[i] for i in range(4))
    
    for i in range(rows):
        for j in range(cols):
            for dx, dy in directions:
                if check_direction(i, j, dx, dy):
                    total += 1
    
    return total


def solve_part_2(grid):
    rows, cols = len(grid), len(grid[0])
    total = 0

    def is_mas(a, b, c):
        return (a + b + c == 'MAS') or (a + b + c == 'SAM')
    
    # For each possible centre
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            # Check top-left to bottom-right diagonal combinations
            tl_to_br = [
                is_mas(grid[i-1][j-1], grid[i][j], grid[i+1][j+1]),  # MAS/SAM from top-left
                is_mas(grid[i+1][j+1], grid[i][j], grid[i-1][j-1])   # MAS/SAM from bottom-right
            ]
            
            # Check top-right to bottom-left diagonal combinations
            tr_to_bl = [
                is_mas(grid[i-1][j+1], grid[i][j], grid[i+1][j-1]),  # MAS/SAM from top-right
                is_mas(grid[i+1][j-1], grid[i][j], grid[i-1][j+1])   # MAS/SAM from bottom-left
            ]
            
            # If we have at least one valid MAS/SAM in each diagonal direction
            if any(tl_to_br) and any(tr_to_bl):
                total += 1
    
    return total


if __name__ == "__main__":
    sample_grid_1 = convert_to_grid(sample_input_1)
    sample_grid_2 = convert_to_grid(sample_input_2)
    actual_grid = convert_to_grid(actual_input)
    assert solve_part_1(sample_grid_1) == 18
    print("Part 1:", solve_part_1(actual_grid))
    assert solve_part_2(sample_grid_2) == 9
    print("Part 2:", solve_part_2(actual_grid))