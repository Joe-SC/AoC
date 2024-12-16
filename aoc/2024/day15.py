"""https://adventofcode.com/2024/day/15"""

from aoc_utils import fetch_input_data
from collections.abc import Iterable


actual_input = fetch_input_data(2024, 15)

MOVE_TO_COORD = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0)
}

def grid_to_str(grid: Iterable[Iterable[str]]) -> str:
    return '\n'.join([''.join(row) for row in grid])

def print_grid(grid: Iterable[Iterable[str]]):
    print(grid_to_str(grid))

def parse_input(inputs: str) -> tuple[Iterable[Iterable[str]], str]:
    starting_grid_str, moves = inputs.split("\n\n")
    starting_grid = [list(row) for row in starting_grid_str.splitlines()]
    return starting_grid, moves

def search_grid(grid: Iterable[Iterable[str]]) -> tuple[tuple[int, int], list[tuple[int, int]], list[tuple[int, int]]]:
    robot = None  # Initialize robot position
    boxes = []
    boundaries = []
    
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '@':
                robot = (x, y)
            elif cell == '0':
                boxes.append((x, y))
            elif cell == '#':
                boundaries.append((x, y))
    
    if robot is None:
        raise ValueError("No robot found in grid")
        
    return robot, boxes, boundaries

def populate_grid(grid: Iterable[Iterable[str]], robot: tuple[int, int], boxes: list[tuple[int, int]], boundaries: list[tuple[int, int]]) -> list[list[str]]:
    grid[robot[1]][robot[0]] = '@'
    for box in boxes:
        grid[box[1]][box[0]] = '0'
    for boundary in boundaries:
        grid[boundary[1]][boundary[0]] = '#'
    return grid

def move_robot(grid: list[list[str]], robot: tuple[int, int], move: str) -> tuple[list[list[str]], tuple[int, int]]:
    """Move the robot and any boxes it pushes in the given direction."""
    dx, dy = MOVE_TO_COORD[move]
    new_x, new_y = robot[0] + dx, robot[1] + dy
    
    # Check if move would hit wall
    if grid[new_y][new_x] == '#':
        return grid, robot
        
    # If there's a box, check if we can push the entire line of boxes
    if grid[new_y][new_x] == 'O':
        # Find all consecutive boxes in this direction
        boxes_to_push = []
        check_x, check_y = new_x, new_y
        while grid[check_y][check_x] == 'O':
            boxes_to_push.append((check_x, check_y))
            check_x, check_y = check_x + dx, check_y + dy
        
        # Check if last position is blocked
        if grid[check_y][check_x] == '#' or grid[check_y][check_x] == 'O':
            return grid, robot
            
        # Move all boxes starting from the furthest one
        for box_x, box_y in reversed(boxes_to_push):
            grid[box_y][box_x] = '.'
            grid[box_y + dy][box_x + dx] = 'O'
    
    # Move robot
    grid[robot[1]][robot[0]] = '.'
    grid[new_y][new_x] = '@'
    
    return grid, (new_x, new_y)

def calculate_gps_coordinates(grid: list[list[str]]) -> int:
    """Calculate the sum of GPS coordinates for all boxes."""
    total = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'O':
                gps = 100 * y + x
                total += gps
    return total

def solve_part1(inputs: str) -> int:
    # Parse input
    grid, moves = parse_input(inputs)
    
    # Clean up moves string - remove newlines and any other whitespace
    moves = moves.strip().replace('\n', '')
    
    # Make working copy of grid
    grid = [list(row) for row in grid]
    
    # Find initial robot position
    robot_pos = None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '@':
                robot_pos = (x, y)
                break
        if robot_pos:
            break
    
    # Process each move
    for move in moves:
        grid, robot_pos = move_robot(grid, robot_pos, move)
    
    # Calculate final GPS coordinates
    return calculate_gps_coordinates(grid)


test_input = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

if __name__ == "__main__":
    assert solve_part1(test_input) == 2028
    print("Part 1:", solve_part1(actual_input))