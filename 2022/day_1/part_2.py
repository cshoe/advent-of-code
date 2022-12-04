INPUT_FILE_PATH = "./input.txt"


def main():
    top_three_elves = []

    # Get the total number of calories carried by each elf
    with open(INPUT_FILE_PATH) as fh:
        total = 0
        for line in fh.readlines():
            try:
                total += int(line)
            except ValueError:
                if len(top_three_elves) < 3:
                    top_three_elves.append(total)
                else:
                    _min = min(top_three_elves)
                    if total > _min:
                        top_three_elves[top_three_elves.index(_min)] = total
                total = 0

    print("Sum of top three calores is: {}".format(sum(top_three_elves)))


if __name__ == "__main__":
    main()
