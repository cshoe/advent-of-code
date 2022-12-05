def calculate_round_score(plays: list[str]) -> int:
    score = 0
    elf_play = ord(plays[0]) - 64
    my_play = ord(plays[1]) - 87

    if elf_play == my_play:
        score = 3
    else:
        if my_play - elf_play in (1, -2):
            score = 6
    return score + my_play


def main():
    score = 0
    with open("input.txt") as fh:
        for line in fh.readlines():
            score += calculate_round_score(line.strip().split(" "))
    print("Total score: {}".format(score))


if __name__ == "__main__":
    main()
