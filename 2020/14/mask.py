import re
import sys

INSTRUCTION_RE = re.compile(r'mem\[(?P<addr>\d+)\] = (?P<val>\d+)')


def _build_mask(mask_str):
    mask = {}
    for i, char in enumerate(mask_str):
        if char in ("0", "1"):
            mask[i] = char
    return mask


def _apply_mask(int_value, mask):
    bit_int_36 = list(bin(int_value)[2:].zfill(36))
    for idx, char in mask.items():
        bit_int_36[idx] = char
    return int(''.join(bit_int_36), 2)


def _sum_memory(memory):
    return sum(memory.values())


def part1(filename):
    memory = {}
    with open(filename) as fh:
        for instruction in fh:
            if instruction.startswith("mask"):
                mask = _build_mask(instruction.split("=")[1].strip())
            else:
                matches = INSTRUCTION_RE.match(instruction)
                if matches is None:
                    continue
                memory[matches.group("addr")] = _apply_mask(int(matches.group("val")), mask)
    return _sum_memory(memory)


def _build_floating_masks(mask_str):
    """
    Return two values, a  bit mask to handle setting 1 bits, an OR operation.
    The second value is a list of all the possible floating bit masks.
    """
    set_bitmask = 0
    float_bitmasks = [0,]
    for char in mask_str:
        #  shift all bits
        set_bitmask = set_bitmask << 1
        float_bitmasks = [m << 1 for m in float_bitmasks]

        if char == '1':
            # set the 1s bit to 1
            set_bitmask |= 1
        elif char == 'X':
            new_float_bitmasks = []
            for m in float_bitmasks:
                # add the 0 case to the list
                new_float_bitmasks.append(m)
                # add the 1 case
                m |= 1
                new_float_bitmasks.append(m)
            float_bitmasks = new_float_bitmasks
    return set_bitmask, float_bitmasks


def part2(filename):
    memory = {}
    with open(filename) as fh:
        for instruction in fh:
            if instruction.startswith("mask"):
                set_mask, floating_masks = _build_floating_masks(instruction.split("=")[1].strip())
            else:
                matches = INSTRUCTION_RE.match(instruction)
                if matches is None:
                    continue
                location = int(matches.group("addr"))
                val = int(matches.group("val"))
                location |= set_mask

                # ANDing with the compliment of the largest mask.
                # This makes sure any possible floating bit in the location is
                # set to 0
                location &= ~ max(floating_masks)
                for mask in floating_masks:
                    masked_location = location | mask
                    memory[masked_location] = val
    return _sum_memory(memory)


if __name__ == '__main__':
    filename = sys.argv[1]
    print(part1(filename))
    #print(part2(filename))
