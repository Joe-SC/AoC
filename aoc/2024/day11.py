"""https://adventofcode.com/2024/day/11"""

from aoc_utils import fetch_input_data
from collections import defaultdict


actual_input = fetch_input_data(2024, 11)
test_input_1 = "0 1 10 99 999"
test_input_2 = "125 17"

def change_stone(stone: str) -> str:
    if stone == "0":
        return "1"
    elif len(stone) % 2 == 0:
        first_half = int(stone[:len(stone)//2])
        second_half = int(stone[len(stone)//2:])
        return f"{first_half} {second_half}"
    else:
        return str(int(stone) * 2024)
    
def change_stones(inputs: str) -> str:
    return " ".join([
        change_stone(stone) 
        for stone in inputs.split()
        ])

def change_stones_n_times(inputs: str, n: int) -> str:
    for _ in range(n):
        inputs = change_stones(inputs)
    return inputs

assert change_stones_n_times(test_input_1, 1) == '1 2024 1 0 9 9 2021976'
assert change_stones_n_times(test_input_2, 6) == "2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2"
assert len(change_stones_n_times(test_input_2, 6).split(" ")) == 22
assert len(change_stones_n_times(test_input_2, 25).split(" ")) == 55312
stone_configuration = change_stones_n_times(actual_input.strip(), 25)
n_stones = len(stone_configuration.split(" "))
print("Part 1:", n_stones)


def update_stones(curr_stones: defaultdict) -> defaultdict:
   changes = defaultdict(int)
   
   for val, count in curr_stones.items():
       # Remove all stones of this value
       changes[val] -= count
       
       # Add new stones based on rules
       if val == 0:
           changes[1] += count
       elif len(str(val)) % 2 == 0:
           left = int(str(val)[:len(str(val))//2])
           right = int(str(val)[len(str(val))//2:])
           changes[left] += count
           changes[right] += count
       else:
           new_val = val * 2024
           changes[new_val] += count
           
   return changes

def change_stones_n_times(inputs: str, n: int) -> int:
   # counting how many of each stone value we have
   curr_stones = defaultdict(int)
   for stone in inputs.split():
       curr_stones[int(stone)] += 1
   
   for _ in range(n):
       # get changes for this iteration
       changes = update_stones(curr_stones)
       for val, change in changes.items():
           curr_stones[val] += change
           if curr_stones[val] == 0:
               curr_stones.pop(val)
               
   return sum(curr_stones.values())


# Part 1
n_stones = change_stones_n_times(actual_input.strip(), 25)
print("Part 1:", n_stones)

# Part 2
n_stones = change_stones_n_times(actual_input.strip(), 75)
print("Part 2:", n_stones)