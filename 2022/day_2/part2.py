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


WINS = {
    "A": "Y",
    "B": "Z",
    "C": "X"
}


LOSSES = {
    "A": "Z",
    "B": "X",
    "C": "Y"
}

DRAWS = {
    "A": "X",
    "B": "Y",
    "C": "Z"
}


def calculate_plays(match: list[str]) -> list[str]:
    result = match[1]
    if result == "Y":
        return [match[0], DRAWS[match[0]]]
    
    if result == "X":
        return [match[0], LOSSES[match[0]]]

    return [match[0], WINS[match[0]]]


def main():
    score = 0
    with open("input.txt") as fh:
        for line in fh.readlines():
            score += calculate_round_score(calculate_plays(line.strip().split(" ")))
    print("Total score: {}".format(score))


if __name__ == "__main__":
    main()
