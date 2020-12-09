import sys

lines = [int(l.rstrip('\n')) for l in sys.stdin]

PREAMBLE_LENGTH = 25


def is_match(start, end, target):
    ptr = 0
    section = lines[start:end]
    for x in range(0, PREAMBLE_LENGTH-1):
        for i, thing in enumerate(section):
            if thing == section[x]:
                continue
            if section[x] + thing == target:
                return True
    return False

def part1():
    ptr = PREAMBLE_LENGTH
    for line in lines[PREAMBLE_LENGTH:]:
        if not is_match(ptr - PREAMBLE_LENGTH, ptr, lines[ptr]):
            print("Answer: {}".format(lines[ptr]))
            return lines[ptr]
        ptr += 1

def part2(target):
    size = 2
    while size < len(lines):
        for i, line in enumerate(lines):
            cont_set = lines[i:i+size]
            if sum(cont_set) == target:
                return min(cont_set) + max(cont_set)
        size += 1
        

if __name__ == '__main__':
    print(part2(part1()))
