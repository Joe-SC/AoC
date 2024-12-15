"""https://adventofcode.com/2024/day/14"""

from aoc_utils import fetch_input_data
import re
import numpy as np 
from collections.abc import Iterable
import tqdm

actual_input = fetch_input_data(2024, 14)
sample_input = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3\
"""

sample_final_grid = """\
......2..1.
...........
1..........
.11........
.....1.....
...12......
.1....1....\
"""

pattern = r'p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)'

def grid_to_str(grid: Iterable[Iterable[str]]) -> str:
    return '\n'.join([''.join(row) for row in grid])

def print_grid(grid: Iterable[Iterable[str]]):
    print(grid_to_str(grid))

def parse_robot(text: str):
    matches = re.match(pattern, text)
    p = (int(matches.group(1)), int(matches.group(2)))
    v = (int(matches.group(3)), int(matches.group(4)))
    return p, v

def initialize_robots(inputs: str) -> tuple[np.ndarray, np.ndarray]:
    robots = [parse_robot(line) for line in inputs.splitlines()]
    p, v = zip(*robots)
    return np.array(p), np.array(v)

def move_robots(p0: np.ndarray, v: np.ndarray,
                space: tuple[int, int]) -> tuple[np.ndarray, np.ndarray]:
    p = p0 + v
    p = np.mod(p, space)
    return p, v

def move_robots_n_steps(p0: np.ndarray, v0: np.ndarray,
                        space: tuple[int, int], n: int) -> np.ndarray:
    p = p0 + (v0 * n)
    p = np.mod(p, space)
    return p

def simulate_robots(p0: np.ndarray, v0: np.ndarray,
                    space: tuple[int, int], steps: int) -> np.ndarray:
    p = p0.copy()
    v = v0.copy()
    p_history = [p]
    for _ in range(steps):
        p, v = move_robots(p, v, space)
        p_history.append(p)
    return p_history

def represent_grid(p: np.ndarray, space: tuple[int, int], fillchar: str=".") -> list[list[str]]:
    grid = [[0 for _ in range(space[0])] for _ in range(space[1])]
    
    # Ensure all coordinates are within bounds using modulo
    x = p[:,0].astype(int) % space[0]
    y = p[:,1].astype(int) % space[1]
    
    # Add robots to grid
    for x_pos, y_pos in zip(x, y):
        grid[y_pos][x_pos] += 1

    # Convert to string representation
    for y in range(space[1]):
        for x in range(space[0]):
            if grid[y][x] > 0:
                grid[y][x] = str(grid[y][x])
            else:
                grid[y][x] = fillchar
    return grid

def safety_factor(p: np.ndarray, space: tuple[int, int]) -> int:
    center_x, center_y = space[0] // 2, space[1] // 2
    x, y = p[:,0], p[:,1]
    
    # Create mask for non-center points
    valid = (x != center_x) & (y != center_y)
    
    quads = [
        ((x[valid] < center_x) & (y[valid] < center_y)).sum(),
        ((x[valid] > center_x) & (y[valid] < center_y)).sum(),
        ((x[valid] < center_x) & (y[valid] > center_y)).sum(),
        ((x[valid] > center_x) & (y[valid] > center_y)).sum()
    ]
    
    return np.prod(quads)


def find_dense_configurations(p_history: list[np.ndarray]) -> list[tuple[int, float]]:
    # Convert list of arrays to 3D array: (timestep, robot_id, coordinate)
    positions = np.stack(p_history)
    
    avg_distances = []
    for t, pos in tqdm.tqdm(enumerate(positions)):
        # Calculate pairwise distances between all robots
        # Using broadcasting to compute differences
        diff = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
        
        # Calculate Euclidean distances
        distances = np.sqrt((diff ** 2).sum(axis=2))
        
        # Create mask to exclude self-distances and lower triangle
        mask = np.triu(np.ones_like(distances), k=1).astype(bool)
        
        # Calculate average distance for this timestep
        avg_distance = distances[mask].mean()
        avg_distances.append((t, avg_distance))
    
    # Sort by average distance
    avg_distances.sort(key=lambda x: x[1])
    return avg_distances


if __name__ == "__main__":
    p0, v0 = initialize_robots(sample_input)
    space = 11, 7
    p_final = move_robots_n_steps(p0, v0, space=space, n=100)
    assert safety_factor(p_final, space=space) == 12
    grid_final = represent_grid(p_final, space=space)
    assert grid_to_str(represent_grid(p_final, space=space)) == sample_final_grid
    # Part 1
    p0, v0 = initialize_robots(actual_input)
    space = 101, 103
    p_final_0 = move_robots_n_steps(p0, v0, space=space, n=100)
    print("Part 1:", safety_factor(p_final_0, space=space))

    # Part 2 - Search first 10000 steps for dense configurations
    p_history = simulate_robots(p0, v0, space=space, steps=10000)
    dense_configurations = find_dense_configurations(p_history)

    # Print top 5 dense configurations
    # Find the Christmas Tree!
    for t, dist in dense_configurations[:5]:
        print(f"step {t}: {dist:.2f}")
        config_grid = represent_grid(p_history[t], space=space)
        print_grid(config_grid)