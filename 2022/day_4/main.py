INPUT_PATH = "input.txt"


def _get_min_max(section: str) -> list[int]:
    return [int(x) for x in section.split("-")]

def apply_filter(filter_func) -> int:
    encompassed_cnt = 0
    with open(INPUT_PATH) as fh:
        for line in fh.readlines():
            elf_sections = line.split(",")
            elf_1 = _get_min_max(elf_sections[0])
            elf_2 = _get_min_max(elf_sections[1])


            if filter_func(elf_1, elf_2):
                encompassed_cnt += 1
    return encompassed_cnt


def _part1_filter(range_1, range_2: list[int]) -> bool:
    return (range_1[0] <= range_2[0] and range_1[1] >= range_2[1]) or \
            (range_2[0] <= range_1[0] and range_2[1] >= range_1[1])


def _part2_filter(range_1, range_2: list[int]) -> bool:
    return ((range_1[0] <= range_2[0] <= range_1[1]) or (range_1[0] <= range_2[1] <= range_1[1])) or \
            ((range_2[0] <= range_1[0] <= range_2[1]) or (range_2[0] <= range_1[1] <= range_2[1]))


def part1():
    print("Encompassed count: {}".format(apply_filter(_part1_filter)))


def part2():
    print("Include count: {}".format(apply_filter(_part2_filter)))


if __name__ == "__main__":
    part1()
    part2()
