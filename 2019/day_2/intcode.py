def run_intcode_program(tape):
    """

    """
    head = 0
    while head < len(tape):
        if tape[head] == 1:
            # addition
            op_1, op_2, store_location = tape[tape[head+1]], tape[tape[head+2]], tape[head+3]
            tape[store_location] = op_1 + op_2
        elif tape[head] == 2:
            # multiplication
            op_1, op_2, store_location = tape[tape[head+1]], tape[tape[head+2]], tape[head+3]
            tape[store_location] = op_1 * op_2
        elif tape[head] == 99:
            print("Halt opcode. Returning tape")
            return tape
        else:
            print("Bad opcode {}. Returning tape".format(tape[head]))
            return tape

        # advance head after addition or multiplication
        head += 4
    print("End of program. Returning tape")
    return tape


def run_1202_alarm(tape):
    return run_noun_verb(tape, 12, 2)


def find_19690720(tape):
    for noun in range(0, 99):
        for verb in range(0, 99):
            result_tape = run_noun_verb(tape[:], noun, verb)
            if result_tape[0] == 19690720:
                return noun, verb
    print("No match")
    return None, None


def run_noun_verb(tape, noun, verb):
    tape[1] = noun
    tape[2] = verb
    return run_intcode_program(tape)


def main():
    program = None
    with open("input") as fh:
        program = fh.readline().strip().split(",")
    program = [int(op) for op in program]
    noun, verb = find_19690720(program)
    print(100 * noun + verb)

if __name__ == '__main__':
    main()
