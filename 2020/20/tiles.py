import itertools
import math
import sys


class Tile(object):
    def __init__(self, lines):
        self.id = lines[0].split(" ")[1].replace(":", "")
        self.top = lines[1]
        self.bottom = lines[-1]
        self.right = ''.join([x[-1] for x in lines[1:]])
        self.left = ''.join([x[0] for x in lines[1:]])

    def rotate(self):
        old_bottom = self.bottom

        self.bottom = self.right[::-1]
        self.right = self.top
        self.top = self.left[::-1]
        self.left = old_bottom


def parse_file(filename):
    with open(filename) as fh:
        contents = fh.read()

        tiles = {}
        for tile in contents.split("\n\n"):
            t = Tile(tile.split("\n"))
            tiles[t.id] = t
    print(tiles)
    return tiles


NEIGHBORS = {
    "top": (0, -1),
    "right": (1, 0),
    "bottom": (0, 1),
    "left": (-1, 0)
}


def part1(filename):
    tile_db = parse_file(filename)
    length = int(math.sqrt(len(tile_db)))

    # This loop generates every permutation fo the tile IDs
    for perm in itertools.permutations(tile_db.keys(), len(tile_db)):
        print("new perm")

        # create a matrix out of the permuation
        layout = []
        for x in range(length):
            layout.append(perm[x*length:(x*length)+length])

        db = tile_db.copy()

        board = []
        first_tile = db[perm[0]]
        # check the first tile in a loop because it needs to be rotated
        for x in range(0, 4):




            for y_idx, row in enumerate(layout):
                row_fits = False
                for x_idx, tile_id in enumerate(row):
                    fits = check_neighbors(x_idx, y_idx, db, tile_id, length, layout)
                    if fits:
                        print("it fits!")
                        continue
                    else:
                        break
                else:
                    row_fits = True

                if row_fits not True:
                    break
            else:
            



def check_neighbors(x_idx, y_idx, db, tile_id, length, layout):
    for k,v in NEIGHBORS.items():
        match = False
        check_x = x_idx + v[0]
        check_y = y_idx + v[1]

        if check_x < 0 or check_y < 0:
            continue

        if check_x >= length or check_y >= length:
            continue

        check_tile = db[layout[check_y][check_x]]
        tile = db[tile_id]

        if k == "top":
            def compare(check_tile, tile):
                return check_tile.bottom == tile.top
        elif k == "right":
            def compare(check_tile, tile):
                return check_tile.left == tile.right
        elif k == "bottom":
            def compare(check_tile, tile):
                return check_tile.top == tile.bottom
        elif k == "left":
            def compare(check_tile, tile):
                return check_tile.right == tile.left

        match = False
        for x in range(0,4):
            if compare(check_tile, tile) == True:
                match = True
                break
            else:
                check_tile.rotate()
        return match


if __name__ == '__main__':
    filename = sys.argv[1]
    part1(filename)
