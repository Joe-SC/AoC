"""https://adventofcode.com/2024/day/7"""

from aoc_utils import fetch_input_data
import logging
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
from itertools import product

logger = logging.getLogger(__name__)
actual_input = fetch_input_data(2024, 7)

sample_input="""\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20\
"""

def generate_patterns(n, symbols = ['+', '*', '|']):
    # Generate all combinations using product
    return [''.join(p) for p in product(symbols, repeat=n)]

def add_to_solution_counter(counter, key):
    if key in counter:
        counter[key] += 1
    else:
        counter[key] = 1

def add_to_solution_bank(bank, key, value):
    if key in bank:
        bank[key].append(value)
    else:
        bank[key] = [value]

def evaluate_part_1(expression):
    expression = expression.replace(" ", "")

    current_num = ""
    result = None
    current_operator = None

    for char in expression:
        if char.isdigit():
            current_num += char
        else: 
            num = int(current_num)
            current_num = ""

            if result is None:
                result = num
            else:
                if current_operator == '+':
                    result += num
                elif current_operator == '*':
                    result *= num
            current_operator = char

    if current_num:
        num = int(current_num)
        if current_operator == '+':
            result += num
        elif current_operator == '*':
            result *= num

    return result

def evaluate_part_2(expression):
    expression = expression.replace(" ", "")

    current_num = ""
    result = None
    current_operator = None
    
    for char in expression:
        if char.isdigit():
            current_num += char
        else: 
            num = int(current_num)
            current_num = ""

            if result is None:
                result = num
            else:
                if current_operator == '+':
                    result += num
                elif current_operator == '*':
                    result *= num
                elif current_operator == '|':
                    # Convert result to string, concatenate with num, then convert back to int
                    result = int(str(result) + str(num))
            current_operator = char

    if current_num:
        num = int(current_num)
        if current_operator == '+':
            result += num
        elif current_operator == '*':
            result *= num
        elif current_operator == '|':
            result = int(str(result) + str(num))

    return result

def evaluate(expression, part):
    match part:
        case 1:
            return evaluate_part_1(expression)
        case 2:
            return evaluate_part_2(expression)

def solve(inputs: str, part: int)->tuple[int, dict, dict]:
    equations_raw = inputs.splitlines()
    solution_counter = {}
    solution_bank = {}
    target_set = set()

    for equation in equations_raw:
        components = equation.split(': ')
        target, equation_str = int(components[0]), components[1]
        space_indexes = [i for i, char in enumerate(equation_str) if char == ' ']
        n_spaces = len(space_indexes)
        for pattern in generate_patterns(n_spaces):
            equation_chars = list(equation_str)
            # fill patern into equation
            for i, char in enumerate(pattern):
                equation_chars[space_indexes[i]] = char
            filled_equation = ''.join(equation_chars)
            if evaluate(filled_equation, part) == target:
                target_set.add(target)
                add_to_solution_counter(solution_counter, equation)
                add_to_solution_bank(solution_bank, equation, filled_equation)

    return sum(target_set), solution_counter, solution_bank


if __name__=="__main__":
    # part 1
    total, solutions, solution_bank = solve(sample_input, part=1)
    assert total == 3749
    total, solutions, solution_bank = solve(actual_input, part=1)
    print("Part 1:",total)

    # part 2
    total, solutions, solution_bank = solve(sample_input, part=2)
    assert total == 11387
    total, solutions, solution_bank = solve(actual_input, part=2)
    print("Part 2:",total)