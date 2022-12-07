INPUT_PATH = "input.txt"

def _calculate_priority(item: str) -> int:
    uni_int = ord(item)
    if uni_int > 96:
        return uni_int - 96
    return uni_int - 38


def part1():
    total = 0
    with open(INPUT_PATH) as fh:
        for line in fh.readlines():
            line = line.strip()
            split_point = int(len(line) / 2)
            comp_1 = line[0:split_point]
            comp_2 = line[split_point:]

            common_item = set(comp_1).intersection(set(comp_2)).pop()
            total += _calculate_priority(common_item)
    print("Total priority: {}".format(total))


def _read_three(fh):
    while True:
        try:
            yield [set(next(fh).strip()) for _ in range(3)]
        except StopIteration:
            return

def part2():
    total = 0
    with open(INPUT_PATH) as fh:
        for lines in _read_three(fh):
            common_item = lines[0].intersection(lines[1], lines[2]).pop()
            total += _calculate_priority(common_item)
    print("Total priority: {}".format(total))


if __name__ == "__main__":
    part1()
    part2()
