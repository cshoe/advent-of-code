import collections
import math
import sys


def _read_input(filename):
    """
    Reads the input file and returns a tuple, first element is an integer
    indicating the earlier possible departure. The second element is a list of
    bus IDs.
    """
    dep_time = None
    bus_ids = None
    with open(filename) as fh:
        dep_time = int(fh.readline())
        bus_ids = [int(i) for i in fh.readline().split(',') if i != "x"]

    return (dep_time, bus_ids)


def _get_soonest_bus(earliest, bus_id):
    """
    Find the timestamp of the soonest departure of ``bus_id``.
    """
    return math.ceil(earliest / bus_id) * bus_id


def _get_possible_bus_schedule(earliest, bus_ids):
    schedule = {}
    for i in bus_ids:
        schedule[i] = _get_soonest_bus(earliest, i)
    return schedule


def _get_fastest_schedule(schedule):
    soonest_bus_id = None
    for bus_id, next_bus in schedule.items():
        if soonest_bus_id == None or next_bus < schedule[soonest_bus_id]:
            soonest_bus_id = bus_id
    return soonest_bus_id, schedule[soonest_bus_id]


def part1(puzzle_input):
    schedule = _get_possible_bus_schedule(puzzle_input[0], puzzle_input[1])
    soonest_bus_id, departure = _get_fastest_schedule(schedule)
    return (departure - puzzle_input[0]) * soonest_bus_id


def _build_offset_mod_table(filename):
    """
    Return a dict that maps bus IDs to a tuple containing (index, mod).
    """
    table = collections.OrderedDict()
    with open(filename) as fh:
        fh.readline()  # don't care about this line
        for i, val in enumerate(fh.readline().split(',')):
            if val == "x":
                continue
            bus_id = int(val)
            table[bus_id] = i
    return table


def part2(filename):
    table = _build_offset_mod_table(filename)
    for i, (bus_id, offset) in enumerate(table.items()):
        if i == 0:
            step = bus_id
            to_try = bus_id
        else:
            mod = -offset % bus_id
            while to_try % bus_id != mod:
                to_try += step 
            else:
                step *= bus_id
    return to_try


if __name__ == '__main__':
    puzzle_input = _read_input(sys.argv[1])
    print(part1(puzzle_input))
    print(part2(sys.argv[1]))
