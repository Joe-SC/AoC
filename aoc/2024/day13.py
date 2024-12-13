"""https://adventofcode.com/2024/day/13"""

from aoc_utils import fetch_input_data
import logging
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
from itertools import product
import re
import math
import numpy as np
from numpy.linalg import solve

logger = logging.getLogger(__name__)
actual_input = fetch_input_data(2024, 13)
sample_input = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279\
"""

def get_xy(text: str):
    numbers =  re.findall(r'\d+', text)
    x, y = int(numbers[0]), int(numbers[1])
    return np.array([x, y])

def parse_machine(machine_str: str):
    button_a_str, button_b_str, prize_str = machine_str.splitlines()
    A, B = get_xy(button_a_str), get_xy(button_b_str)
    C = get_xy(prize_str)
    return A, B, C

def solve_machine_optimized(A: np.ndarray, 
                            B: np.ndarray, 
                            C: np.ndarray,):
    
    # First get the float solution to have an idea of the range
    coeffs = np.column_stack((A, B))
    try:
        a_float, b_float = solve(coeffs, C)
    except np.linalg.LinAlgError:
        return None
    
    # If the float solutions are negative or very large, we can return early
    if a_float < 0 or b_float < 0:
        return None
    
    # Search around the float solution
    a_start = max(1, math.floor(a_float - 5))
    a_end = math.ceil(a_float + 5)
    b_start = max(1, math.floor(b_float - 5))
    b_end = math.ceil(b_float + 5)
    
    for a in range(a_start, a_end + 1):
        for b in range(b_start, b_end + 1):
            if np.array_equal(a * A + b * B, C):
                return a, b
    
    return None

def solve_machines_part1(inputs: str) -> int:
    machines = inputs.split("\n\n")
    cost = 0
    for machine in machines:
        A, B, C = parse_machine(machine)
        solution = solve_machine_optimized(A, B, C)
        if solution:
            a, b = solution[0], solution[1]
            cost += 3*a+b
    return cost

def solve_machines_part2(inputs: str) -> int:
    machines = inputs.split("\n\n")
    cost = 0
    for machine in machines:
        A, B, C = parse_machine(machine)
        C += 10000000000000
        solution = solve_machine_optimized(A, B, C)
        if solution:
            a, b = solution[0], solution[1]
            cost += 3*a+b
    return cost

if __name__ == "__main__":
    assert solve_machines_part1(sample_input) == 480
    print('Part 1:', solve_machines_part1(actual_input))
    print('Part 2:', solve_machines_part2(actual_input))
