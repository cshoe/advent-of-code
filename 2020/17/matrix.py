import itertools
import sys


ACTIVE = "#"
INACTIVE = "."


def neighbor_step_gen(dimensions):
    zero_value = tuple([0 for x in range(0, dimensions)])
    gen = itertools.product((-1,0,1), repeat=dimensions)
    while True:
        try:
            next_val = next(gen)
        except StopIteration:
            return
        else:
            if next_val != zero_value:
                yield next_val


def get_neighbors(coords):
    # coords = (x, y, z...)
    neighbors = []
    for s in neighbor_step_gen(len(coords)):
        n = []
        for idx, coord in enumerate(coords):
            n.append(coord + s[idx])
        neighbors.append(tuple(n))
    return neighbors


def lookup(active_coords, coords):
    if coords in active_coords:
        return ACTIVE
    else:
        return INACTIVE


def generate_coords_to_test(ranges):
    return itertools.product(*[list(range(r[0], r[1])) for r in ranges])


def get_all_neighbors_state(grids, coords):
    neighbors = get_neighbors(coords)
    neighbor_states = []
    for n in neighbors:
        neighbor_states.append(lookup(grids, n))
    return neighbor_states


def cycle(active_coords):
    if len(active_coords) == 0:
        print("No active coords found")
        return

    dimensions = len(active_coords[0])
    coord_lists = [[] for x in range(dimensions)]
    for coords in active_coords:
        for idx, c in enumerate(coords):
            coord_lists[idx].append(c)

    coord_sets = [set(x) for x in coord_lists]

    ranges = []
    for c_set in coord_sets:
        ranges.append((min(c_set)-1, max(c_set)+2))

    new_active_coords = []

    for coords in generate_coords_to_test(ranges):
        current_state = lookup(active_coords, coords)
        n_states = get_all_neighbors_state(active_coords, coords)
        if current_state == ACTIVE:
            if n_states.count(ACTIVE) in (2, 3):
                new_active_coords.append(coords)
        elif current_state == INACTIVE:
            if n_states.count(ACTIVE) == 3:
                new_active_coords.append(coords)
    return new_active_coords


def part1(filename):
    active_coords = []
    with open(filename) as fh:
        for y_idx, line in enumerate(fh):
            for x_idx, char in enumerate(line):
                if char == ACTIVE:
                    active_coords.append((x_idx, y_idx, 0))

    for x in range(0,6):
        active_coords = cycle(active_coords)
    print(len(active_coords))


def part2(filename):
    active_coords = []
    with open(filename) as fh:
        for y_idx, line in enumerate(fh):
            for x_idx, char in enumerate(line):
                if char == ACTIVE:
                    active_coords.append((x_idx, y_idx, 0, 0))

    for x in range(0,6):
        active_coords = cycle(active_coords)
    print(len(active_coords))



if __name__ == '__main__':
    filename = sys.argv[1]
    part1(filename)
    part2(filename)
