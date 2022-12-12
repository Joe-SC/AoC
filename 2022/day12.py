"""https://adventofcode.com/2022/day/12"""
import os

from heapq import heappop, heappush
from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day12_input.txt")) as f:
    actual_input = f.read()


sample_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

XY = tuple[int, int]


def manhattan_distance(a: XY, b: XY):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


@print_time_taken
def solve(inputs: str) -> None:
    start, target = (0, 0), (0, 0)
    grid: dict[XY, int] = {}
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            xy, elevation = (x, y), ord(c) - ord("a")
            if c == "S":
                start, elevation = xy, 0
            elif c == "E":
                target, elevation = xy, 25
            grid[xy] = elevation

    possible_steps = {}
    for xy in grid:
        steps = []
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            step = (xy[0] + dx, xy[1] + dy)
            if grid.get(step, 999) - grid[xy] <= 1:
                steps.append(step)
        possible_steps[xy] = tuple(steps)

    def shortest_path(start: XY) -> int:
        visited: set[XY] = set()
        distance_to = {start: 0}
        to_visit: list[tuple[float, XY]] = []
        heappush(to_visit, (0, start))
        while to_visit:
            _, this_node = heappop(to_visit)
            if this_node == target:
                return distance_to[this_node]
            visited.add(this_node)
            for next_node in possible_steps[this_node]:
                distance_to_here = distance_to[this_node] + 1
                prior_distance_to_here = distance_to.get(next_node, 0)
                if next_node in visited and distance_to_here >= prior_distance_to_here:
                    continue
                if distance_to_here < prior_distance_to_here or next_node not in [
                    i[1] for i in to_visit
                ]:
                    distance_to[next_node] = distance_to_here
                    h_score = manhattan_distance(target, next_node) - grid[next_node]
                    f_score = distance_to_here + h_score
                    heappush(to_visit, (f_score, next_node))
        raise ValueError("No path found")

    path_length = shortest_path(start)
    print(f"Part 1: {path_length}")

    first_steps = {
        s
        for s, e in grid.items()
        if e == 1 and any(grid[n] == 0 for n in possible_steps[s])
    }
    path_lengths = (shortest_path(first_step) + 1 for first_step in first_steps)
    print(f"Part 2: {min(path_lengths)}\n")


solve(sample_input)
solve(actual_input)
