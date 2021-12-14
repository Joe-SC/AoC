from collections import Counter
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day14_input.txt")) as f:
    actual_input = f.read()

sample_input = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def solve(inputs):
    template_polymer, replacements = inputs.split('\n\n')
    replacements = dict(tuple(r.split(" -> ")) for r in replacements.splitlines())
    
    def get_answer(steps):
        elements = Counter(template_polymer)
        pair_counts = { ab: template_polymer.count(ab) for ab in replacements }
        for _ in range(steps):
            new_pair_counts = Counter()
            for (a, b), x in replacements.items():
                elements[x] += pair_counts[a + b]
                new_pair_counts[a + x] += pair_counts[a + b]
                new_pair_counts[x + b] += pair_counts[a + b]
            pair_counts = new_pair_counts

        return max(elements.values()) - min(elements.values())

    print(f'Part 1: {get_answer(10)}')
    print(f'Part 2: {get_answer(40)}\n')


solve(sample_input)
solve(actual_input)
