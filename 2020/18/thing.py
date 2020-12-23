import re
import sys


MULTIPLICATION_RE = re.compile(r'(\d+)([\*])(\d+)')
ADDITION_RE = re.compile(r'(\d+)([\+])(\d+)')
OPERATE_RE = re.compile(r'(\d+)([\*\+])(\d+)')
INNER_PARENS = re.compile(r'\(\d+[\*\+]\d+[\d\+\*]*\)')


def operate(m):
    op_1 = int(m.group(1))
    op_2 = int(m.group(3))

    if m.group(2) == "+":
        return str(op_1 + op_2)
    elif m.group(2) == "*":
        return str(op_1 * op_2)
    else:
        return


def addition_first_collapse_parens(m):
    inside_parens = m.group()[1:-1]
    subs_made = 1
    while subs_made > 0:
        inside_parens, subs_made = ADDITION_RE.subn(operate, inside_parens, count=1)

    subs_made = 1
    while subs_made > 0:
        inside_parens, subs_made = MULTIPLICATION_RE.subn(operate, inside_parens, count=1)
    return inside_parens


def collapse_parens(m):
    OPERATE_RE = re.compile(r'(\d+)([\*\+])(\d+)')

    inside_parens = m.group()[1:-1]
    subs_made = 1
    while subs_made > 0:
        inside_parens, subs_made = OPERATE_RE.subn(operate, inside_parens, count=1)

    return inside_parens


def part1(filename):
    total = 0
    with open(filename) as fh:
        for line in fh:
            line = line.replace(" ", "").strip()

            subs_made = 1
            while subs_made > 0:
                line, subs_made = INNER_PARENS.subn(collapse_parens, line, count=1)

            line = line.replace("(", "").replace(")", "")

            subs_made = 1
            while subs_made > 0:
                line, subs_made = OPERATE_RE.subn(operate, line, count=1)

            total += int(line)
    print("Part 1 total: {}".format(total))


def part2(filename):
    total = 0
    with open(filename) as fh:
        for line in fh:
            line = line.replace(" ", "").strip()

            subs_made = 1
            while subs_made > 0:
                line, subs_made = INNER_PARENS.subn(addition_first_collapse_parens, line, count=1)

            line = line.replace("(", "").replace(")", "")

            subs_made = 1
            while subs_made > 0:
                line, subs_made = ADDITION_RE.subn(operate, line, count=1)

            subs_made = 1
            while subs_made > 0:
                line, subs_made = MULTIPLICATION_RE.subn(operate, line, count=1)

            total += int(line)
    print("Part 2 total: {}".format(total))


if __name__ == '__main__':
    filename = sys.argv[1]
    part1(filename)
    part2(filename)
