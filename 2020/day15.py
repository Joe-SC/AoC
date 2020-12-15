sample_input = [0, 3, 6]
actual_input = [18, 11, 9, 0, 5, 1]


def play_game(seeds, max_rounds):
    last_seen = {n: t for t, n in enumerate(seeds, 1)}
    previous_number = seeds[-1]
    for last_turn in range(len(seeds), max_rounds):
        next_number = last_turn - last_seen.get(previous_number, last_turn)
        last_seen[previous_number] = last_turn
        previous_number = next_number
    return previous_number


def solve(inputs):
    print(f"Part 1: {play_game(inputs, 2020)}")
    print(f"Part 2: {play_game(inputs, 30000000)}\n")


solve(sample_input)
solve(actual_input)
