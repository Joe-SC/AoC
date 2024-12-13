from aoc_utils import fetch_input_data
import logging
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
from itertools import product

logger = logging.getLogger(__name__)

def convert_to_grid(inputs: str, astype:str = 'str') -> list[list[int]]:
    if astype == 'int':
        return [[int(c) for c in row] for row in inputs.splitlines()]
    elif astype == 'str':
        return [[c for c in row] for row in inputs.splitlines()]

def grid_to_str(grid: list[list[str]]) -> str:
    return '\n'.join([''.join(row) for row in grid])

def find_plant_clusters(grid: list[list[str]], target: str) -> list[list[tuple[int, int]]]:
    clusters = []
    seen = set()
    
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == target and (x, y) not in seen:
                cluster = find_plant_cluster(grid, (x, y), target)
                if cluster:  # Only add if we found a cluster
                    clusters.append(cluster)
                    seen.update(cluster)  # Mark all positions in this cluster as seen
                    
    return clusters

def find_plant_cluster(grid: list[list[str]], start: tuple[int, int], plant: str) -> list[tuple[int, int]]:
    cluster = []
    seen = set()
    stack = [start]
    
    while stack:
        pos = stack.pop()
        if pos in seen:
            continue
            
        x, y = pos
        if (x < 0 or x >= len(grid[0]) or 
            y < 0 or y >= len(grid) or
            grid[y][x] != plant):
            continue
            
        seen.add(pos)
        cluster.append(pos)
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (x + dx, y + dy)
            if next_pos not in seen:
                stack.append(next_pos)
                
    return cluster

def calculate_area_perimeter(grid: list[list[str]], cluster: list[tuple[int, int]]) -> tuple[int, int]:
    area = len(cluster)
    perimeter = 0
    cluster_set = set(cluster)
    
    for x, y in cluster:
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (ny < 0 or ny >= len(grid) or 
                nx < 0 or nx >= len(grid[0]) or 
                (nx, ny) not in cluster_set):
                perimeter += 1
    
    return area, perimeter

def calculate_total_price(grid: list[list[str]]) -> int:
    total_price = 0
    seen_positions = set() 
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) in seen_positions: continue
                
            plant = grid[y][x]
            cluster = find_plant_cluster(grid, (x, y), plant)
            
            if not cluster: continue
                
            seen_positions.update(cluster)
            
            area, perimeter = calculate_area_perimeter(grid, cluster)
            price = area * perimeter
            total_price += price
            
    return total_price

def solve_part_1 (input_data: str) -> int:
    grid = convert_to_grid(input_data)
    return calculate_total_price(grid)

if __name__ == "__main__":
    actual_input = fetch_input_data(2024, 12)
    print(solve_part_1(actual_input))
    