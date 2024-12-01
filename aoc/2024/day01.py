"""https://adventofcode.com/2024/day/1"""

from collections import Counter
from aoc_utils import fetch_input_data

actual_input = fetch_input_data(2024, 1)
sample_input = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""


def solve(inputs: str):
    list_a, list_b = [], []
    for line in inputs.splitlines():
        a, b = map(int, line.split())
        list_a.append(a)
        list_b.append(b)
    list_a_sorted = sorted(list_a)
    list_b_sorted = sorted(list_b)
    distance, similarity = 0, 0
    for a, b in zip(list_a_sorted, list_b_sorted):
        distance += abs(a - b)
        similarity += sum([b for b in list_b_sorted if b == a])

    print(f"Distance: {distance}")
    print(f"Similarity: {similarity}")
    return

if __name__ == "__main__":
    solve(sample_input)
    solve(actual_input)
