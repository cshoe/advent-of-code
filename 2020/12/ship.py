import sys

DIRECTIONS = "NESW"

class Ship(object):
    def __init__(self):
        self._current_dir = "E"
        self._movement = {
            "N": 0,
            "E": 0,
            "S": 0,
            "W": 0
        }

    def move(self, direction):
        movement = direction[0]
        val = int(direction[1:])
        getattr(self, movement)(val)

    def N(self, val):
        cur = self._movement["N"]
        self._movement["N"] = cur + val

    def E(self, val):
        cur = self._movement["E"]
        self._movement["E"] = cur + val

    def S(self, val):
        cur = self._movement["S"]
        self._movement["S"] = cur + val

    def W(self, val):
        cur = self._movement["W"]
        self._movement["W"] = cur + val

    def F(self, val):
        cur = self._movement[self._current_dir]
        self._movement[self._current_dir] = cur + val

    def R(self, val):
        dirs_to_rotate = int(val / 90)
        cur_index = DIRECTIONS.index(self._current_dir)
        self._current_dir = DIRECTIONS[(dirs_to_rotate + cur_index) % 4]

    def L(self, val):
        dirs_to_rotate = int(val / 90)
        cur_index = DIRECTIONS.index(self._current_dir)
        self._current_dir = DIRECTIONS[(cur_index - dirs_to_rotate) % 4]

    def manhattan_distance(self):
        return abs(self._movement["E"] - self._movement["W"]) + \
            abs(self._movement["N"] - self._movement["S"])


class Waypoint(object):
    def __init__(self):
        self.coords = {"N": 1, "E": 10}

    def r_rotate(self, degrees):
        dirs_to_rotate = int(degrees / 90)
        new_coords = {}
        for card_dir, vector in self.coords.items():
            cur_index = DIRECTIONS.index(card_dir)
            new_dir = DIRECTIONS[(dirs_to_rotate + cur_index) % 4]
            new_coords[new_dir] = vector
        self.coords = new_coords

    def l_rotate(self, degrees):
        dirs_to_rotate = int(degrees / 90)
        new_coords = {}
        for card_dir, vector in self.coords.items():
            cur_index = DIRECTIONS.index(card_dir)
            new_dir = DIRECTIONS[(cur_index - dirs_to_rotate) % 4]
            new_coords[new_dir] = vector
        self.coords = new_coords


class WaypointShip(Ship):
    def __init__(self):
        self._movement = {
            "N": 0,
            "E": 0,
            "S": 0,
            "W": 0
        }
        self._wp = Waypoint()

    def F(self, val):
        for card_dir, vector in self._wp.coords.items():
            cur_value = self._movement[card_dir]
            self._movement[card_dir] = cur_value + (val * vector)

    def N(self, val):
        if "N" in self._wp.coords:
            self._wp.coords["N"] += val
        elif "S" in self._wp.coords:
            self._wp.coords["S"] -= val

    def E(self, val):
        if "E" in self._wp.coords:
            self._wp.coords["E"] += val
        elif "W" in self._wp.coords:
            self._wp.coords["W"] -= val

    def S(self, val):
        self.N(-val)

    def W(self, val):
        cur = self.E(-val)

    def R(self, val):
        self._wp.r_rotate(val)

    def L(self, val):
        self._wp.l_rotate(val)


def part1(dirctions):
    s = Ship()
    for d in directions:
        s.move(d)
    return s.manhattan_distance()


def part2(directions):
    s = WaypointShip()
    for d in directions:
        s.move(d)
    return s.manhattan_distance()


if __name__ == '__main__':
    directions = [l.rstrip('\n') for l in sys.stdin]
    print(part1(directions))
    print(part2(directions))
