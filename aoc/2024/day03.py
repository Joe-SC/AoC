"""https://adventofcode.com/2024/day/3"""

from aoc_utils import fetch_input_data
import logging
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
import re

logger = logging.getLogger(__name__)

actual_input = fetch_input_data(2024, 3)
sample_input_1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
sample_input_2="xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

def solve_part_1(inputs: str) -> int:
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'    
    total = 0
    for m in re.finditer(pattern, inputs):
        total += int(m.group(1)) * int(m.group(2))
    return total

def solve_part_2(inputs: str) -> int:
    pattern = r'(?:mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\))'
    total = 0
    toggle = 1
    for m in re.finditer(pattern, inputs):
        if m.group(0).startswith('don'):
            logger.debug(f"m.group(0): {m.group(0)}")
            toggle = 0
            logger.debug(f"toggle: {toggle}")
        elif m.group(0).startswith('do'):
            logger.debug(f"m.group(0): {m.group(0)}")
            toggle = 1
            logger.debug(f"toggle: {toggle}")
        elif m.group(0).startswith('mul'):
            logger.debug(f"m.group(0): {m.group(0)}")
            total += toggle * int(m.group(1)) * int(m.group(2))
    return total

if __name__ == "__main__":
    # Part 1
    assert solve_part_1(sample_input_1) == 161  
    print("Part 1:", solve_part_1(actual_input))
    # Part 2
    assert solve_part_2(sample_input_2) == 48
    print("Part 2:", solve_part_2(actual_input))
