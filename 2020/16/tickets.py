import re
import sys


LIMITS_RE = re.compile(r'(?P<field>[\s\w]+): (?P<small_low>\d+)\-(?P<small_high>\d+) or (?P<big_low>\d+)\-(?P<big_high>\d+)')
TICKET_RE = re.compile(r'(\d+,)+\d+')


def find_ranges(fh, field_filter=None):
    ranges = {}
    for line in fh:
        if len(line.strip()) == 0:
            break

        matches = LIMITS_RE.search(line)
        if matches is None:
            continue

        add = True
        if field_filter is not None:
            add = field_filter(matches.group("field"))

        if add is True:
            rs = []
            rs.append((
                int(matches.group("small_low")),
                int(matches.group("small_high"))
            ))

            rs.append((
                int(matches.group("big_low")),
                int(matches.group("big_high"))
            ))
            ranges[matches.group("field")] = rs
    return ranges


def check_nearby_tickets(tickets, ranges):
    error_rate = 0
    valid_tickets = []

    for ticket in tickets:
        valid = True
        for num in ticket:
            for k, rs in ranges.items():
                if (num >= rs[0][0] and num <= rs[0][1]) or (num >= rs[1][0] and num <= rs[1][1]):
                    break
            else:
                valid = False
                error_rate += num
        if valid:
            valid_tickets.append(ticket)
    return (error_rate, valid_tickets)


def part1(filename):
    tickets = load_tickets(filename)
    with open(filename) as fh:
        ranges = find_ranges(fh)

        for line in fh:
            if len(line.strip()) == 0:
                break

        print("Part 1 Error Rate: {}".format(check_nearby_tickets(tickets, ranges)[0]))


def load_tickets(filename):
    with open(filename) as fh:
        tickets = []
        for line in fh:
            if TICKET_RE.search(line) is None:
                continue
            tickets.append([int(i) for i in line.split(',')])
        return tickets


def part2(filename):
    tickets = load_tickets(filename)
    with open(filename) as fh:
        ranges = find_ranges(fh)
        valid_tickets = check_nearby_tickets(tickets, ranges)[1]
        width = len(valid_tickets[0])
        matches = {}

        for k, rs in ranges.items():
            for idx in range(0, width):
                for ticket in valid_tickets:
                    num = ticket[idx]

                    if not ((num >= rs[0][0] and num <= rs[0][1]) or (num >= rs[1][0] and num <= rs[1][1])):
                        break
                else:
                    if k in matches:
                        matches[k].append(idx)
                    else:
                        matches[k] = [idx,]

        finished_matches = {}
        edited = True
        while edited:
            for k, v in matches.items():
                if len(v) == 1:
                    for k_1, v_1 in matches.items():
                        if v[0] in v_1 and len(v_1) > 1:
                            v_1.remove(v[0])
                    finished_matches[k] = matches.pop(k)[0]
                    break
            else:
                edited = False
        dep_nums = [valid_tickets[0][i] for k, i in finished_matches.items() if k.startswith("departure")]
        result = 1
        for num in dep_nums:
            result = result * num
        print("Part 2 product of departure numbers: {}".format(result))


if __name__ == '__main__':
    filename = sys.argv[1]
    part1(filename)
    part2(filename)
