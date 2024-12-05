"""https://adventofcode.com/2024/day/5"""

from aoc_utils import fetch_input_data
import logging
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
import re

logger = logging.getLogger(__name__)
actual_input = fetch_input_data(2024, 5)
sample_input="""\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47\
"""

def parse_inputs(inputs: str):
    [rules_raw, finger_in_your_bussy] = inputs.split("\n\n")

    rules = [rule.split("|") for rule in rules_raw.split("\n")]
    updates = [update.split(",") for update in finger_in_your_bussy.split("\n")]

    # convert to ints
    rules = [[int(x) for x in rule] for rule in rules]
    updates = [[int(p) for p in pages] for pages in updates]
    return rules, updates

def rule_applies(rule: list[str], update: list[str]) -> bool:
    update = set(update)
    rule = set(rule)
    return rule.issubset(update)

def rule_compliant(rule: list[str], updates: list[list[str]]) -> bool:
    """check if the first rule is before the second rule in the list of updates"""
    first_number_index = updates.index(rule[0])
    second_number_index = updates.index(rule[1])
    if first_number_index < second_number_index:
        logger.debug(f"'{rule[0]}' is before {rule[1]}")
        logger.debug(f"rule {rule} is compliant with updates {updates}")
        return True
    else:
        logger.debug(f"rule {rule} is not compliant with updates {updates}")
        logger.debug(f"'{rule[0]}' is after {rule[1]}")
        return False

def correct_update(rules: list[list[str]], update: list[str]) -> bool:
    for rule in rules:
        logger.debug(f"checking rule {rule} against update {update}")
        if rule_applies(rule, update):
            logger.debug(f"rule {rule} applies to update {update}")
            if rule_compliant(rule, update):
                logger.debug(f"rule {rule} is compliant with update {update}")
            else:
                return False
        else:
            logger.debug(f"rule {rule} does not apply to update {update}")
    return True

def middle_element(array: list,) -> list:
    midpoint = len(array) // 2
    return array[midpoint]

def reorder_incorrect_update(rules: list[list[str]], update: list[list[str]]) -> list[list[str]]:
    while not correct_update(rules, update):
        for rule in rules:
            if rule_applies(rule, update):
                first_number_index = update.index(rule[0])
                second_number_index = update.index(rule[1])
                if first_number_index > second_number_index:
                    update[first_number_index], update[second_number_index] = update[second_number_index], update[first_number_index]
    return update

def sum_updates(rules: list[list[str]], updates: list[list[str]]) -> int:
    correct_updates = []
    incorrect_updates = []
    total = 0
    for i, update in enumerate(updates):
        logger.debug(f"checking update {i}: {update}")
        if correct_update(rules, update):
            logger.debug(f"update {i} is correct")
            correct_updates.append(update)
            total += middle_element(update)
        else:
            logger.debug(f"update {i} is incorrect")
            incorrect_update = update[:]
            incorrect_updates.append(incorrect_update)

    return total, correct_updates, incorrect_updates


if __name__ == "__main__":
    sample_rules, sample_updates = parse_inputs(sample_input)
    rules, updates = parse_inputs(actual_input.strip())
    # examples
    assert correct_update(sample_rules, sample_updates[0])
    assert not correct_update(sample_rules, sample_updates[3])
    sample_total, sample_correct_updates, sample_incorrect_updates = sum_updates(sample_rules, sample_updates)
    assert sample_total == 143 
    assert sample_correct_updates == [
        [75, 47, 61, 53, 29], 
        [97, 61, 53, 29, 13], 
        [75, 29, 13]
    ]
    assert reorder_incorrect_update(sample_rules, sample_incorrect_updates[0]) == [97,75,47,61,53]
    assert reorder_incorrect_update(sample_rules, sample_incorrect_updates[1]) == [61,29,13]
    assert reorder_incorrect_update(sample_rules, sample_incorrect_updates[2]) == [97,75,47,29,13]

    correct_total, correct_updates, incorrect_updates = sum_updates(rules, updates)
    corrected_total = 0
    for incorrect_update in incorrect_updates:
        corrected_update = reorder_incorrect_update(rules, incorrect_update)
        if correct_update(rules, corrected_update):
            corrected_total += middle_element(corrected_update)
    print("Correct Total", correct_total)
    print("Corrected Total", corrected_total)