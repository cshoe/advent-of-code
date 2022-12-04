INPUT_FILE_PATH = "./input.txt"


def main():
    max_calories = 0

    # Get the total number of calories carried by each elf
    with open(INPUT_FILE_PATH) as fh:
        total = 0
        for line in fh.readlines():
            try:
                total += int(line)
            except ValueError:
                if total > max_calories:
                    max_calories = total
                total = 0

    print("Most calories is: {}".format(max_calories))


if __name__ == "__main__":
    main()
