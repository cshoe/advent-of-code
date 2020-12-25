import re
import sys


CHARS = ('"a"', '"b"')


cache = {}


def process_rules(rules, pointer, update=True):

    rule = rules[pointer]
    decoded_rule = []
    if update is True:
        if pointer == 8:
            rule_42 = "({})+".format(process_updated_rules(rules, 42))
            cache[pointer] = rule_42
            return rule_42
        elif pointer == 11:
            pattern_42 = process_updated_rules(rules, 42)
            pattern_31 = process_updated_rules(rules, 31)

            for i in range(1, 15):
                decoded_rule.append('(' + f'({pattern_42}){ {i} }' + f'({pattern_31}){ {i} }' + ')')
            rule = '|'.join(decoded_rule)
            cache[pointer] = rule
            return rule

    if pointer in cache:
        return cache[pointer]
    for char in rule:
        if char ==  "|":
            decoded_rule.append(char)
        elif char in CHARS:
            return char[1]
        else:
            next_rule = int(char)
            decoded_rule.append(process_rules(rules, next_rule, update=update))
    rule = "({})".format(''.join(decoded_rule))
    cache[pointer] = rule
    return rule


def part1(filename):
    global cache
    with open(filename) as fh:
        rules = {}
        valid = 0
        for line in fh:
            if len(line.strip()) == 0:
                break
            line.strip('"')
            splits = line.split(":")
            rules[int(splits[0].strip())] = splits[1].strip().split(" ")
        regex = process_rules(rules, 0, update=False)
        regex = re.compile(r"{}".format(regex))

        for line in fh:
            m = regex.fullmatch(line.strip())
            if m is not None:
                valid += 1
        print("Part 1 valid messages: {}".format(valid))
    cache = {}


def part2(filename):
    global cache
    with open(filename) as fh:
        rules = {}
        valid = 0
        for line in fh:
            if len(line.strip()) == 0:
                break
            line.strip('"')
            splits = line.split(":")
            rules[int(splits[0].strip())] = splits[1].strip().split(" ")
        process_rules(rules, 0)

        rule_0 = "({})({})".format(cache[8], cache[11])
        regex = re.compile(rule_0)

        valid = 0
        for line in fh:
            m = regex.fullmatch(line.strip())
            if m is not None:
                valid += 1
        print("Part 2 valid messages: {}".format(valid))
    cache = {}


if __name__ == '__main__':
    filename = sys.argv[1]
    part1(filename)
    part2(filename)
