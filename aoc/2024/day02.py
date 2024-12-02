"""https://adventofcode.com/2024/day/2"""

from aoc_utils import fetch_input_data
import logging

logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

sample_input = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9\
"""

def parse_input(input_data: str) -> list[list[int]]:
    return [[int(x) for x in row.split()] for row in input_data.splitlines()]

def is_same_sign(diffs: list[int]) -> bool:
    logger.debug('all_positive: %s', all(diffs[0] * x > 0 for x in diffs))
    logger.debug('all_negative: %s', all(diffs[0] * x < 0 for x in diffs))
    return (
        all(diffs[0] * x > 0 for x in diffs) or 
        all(diffs[0] * x < 0 for x in diffs)
        )

def is_between(diffs: list[int], lower: int=1, upper: int=3) -> bool:
    logger.debug('value checks: %s', [lower <= abs(x) <= upper for x in diffs])
    logger.debug('all between %d, %d: %s', lower, upper, all(lower <= abs(x) <= upper for x in diffs))
    return all(lower <= abs(x) <= upper for x in diffs)

def is_safe(report: list[int]) -> bool:
    diffs = [report[i+1]-report[i] for i in range(len(report)-1)]
    logger.debug('diffs: %s', diffs)
    return is_same_sign(diffs) and is_between(diffs)


def solve_part_1(inputs: str):
    reports = parse_input(inputs)
    n_safe = 0
    for report in reports:
        logger.debug('Processing report: %s', report)
        if is_safe(report):
            logger.debug('Report marked as safe')
            n_safe += 1
    
    print('Number of safe reports:', n_safe)
    return n_safe


def is_safe_when_dampened(report: list[int]):
    for i in range(len(report)):
        dampened_report = report[:]
        dampened_report.pop(i)
        if is_safe(dampened_report):
            return True


def solve_part_2(inputs: str):
    reports = parse_input(inputs)
    n_safe = 0
    for report in reports:
        logger.debug('Processing report: %s', report)
        if is_safe(report):
            logger.debug('Report marked as safe')
            n_safe += 1
        elif is_safe_when_dampened(report):
            logger.debug('Report marked as safe when dampened')
            n_safe += 1
        
    print('Number of safe reports:', n_safe)
    return n_safe


if __name__ == "__main__":
    print("Sample Input")
    print("------------")
    assert solve_part_1(sample_input) == 2
    assert solve_part_2(sample_input) == 4
    print("\nActual Input")
    print("------------")
    actual_input = fetch_input_data(2024, 2)
    solve_part_1(actual_input)
    solve_part_2(actual_input)