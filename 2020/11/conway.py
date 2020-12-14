import sys

def _build_board(): 
    return [list(l.strip()) for l in sys.stdin]

ADJACENT_DELTAS = [
    (-1,-1), (0,-1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1,1),
] 

def _get_adjacent_seats(x, y, board):
    adjacent_seats = ""
    height = len(board)
    width = len(board[0])
    for d in ADJACENT_DELTAS:
        new_x = x + d[0]
        new_y = y + d[1]
        if (new_x < 0 or new_x >= height) or (new_y < 0 or new_y >= width):
            continue
        adjacent_seats += board[new_x][new_y]
    return adjacent_seats

def _get_visible_seats(x, y, board):
    visible_seats = ""
    height = len(board)
    width = len(board[0])
    for d in ADJACENT_DELTAS:
        new_x = x
        new_y = y
        while True:
            new_x = new_x + d[0]
            new_y = new_y + d[1]
            if (new_x < 0 or new_x >= height) or (new_y < 0 or new_y >= width):
                break
            seat = board[new_x][new_y]
            if seat == ".":
                continue
            visible_seats += seat
            break
    return visible_seats


def _count_occupied_seats(board):
    occupied_seats = 0
    for row in board:
        occupied_seats += row.count("#")
    return occupied_seats

def _play_game(board, other_seats_finder, threshold=4):
    changed = False
    new_board = []
    for row, seat_assignments in enumerate(board):
        new_row = []
        for column, current_seat in enumerate(seat_assignments):
            if current_seat == ".":
                new_row.append(".")
            else:
                other_seats = other_seats_finder(row, column, board)
                if current_seat== "L":
                    if other_seats.count("#") == 0:
                        new_row.append("#")
                        changed = True
                        continue
                elif current_seat == "#":
                    if other_seats.count("#") >= threshold:
                        new_row.append("L")
                        changed = True
                        continue
                new_row.append(current_seat)
        new_board.append(new_row)
    return changed, new_board

def part2(board):
    changed, new_board = _play_game(board, _get_visible_seats, 5)
    while changed:
        changed, new_board = _play_game(new_board, _get_visible_seats, 5)
    return _count_occupied_seats(new_board)


def part1(board):
    changed, new_board = _play_game(board, _get_adjacent_seats, 4)
    while changed:
        changed, new_board = _play_game(new_board, _get_adjacent_seats, 4)

    return _count_occupied_seats(new_board)


if __name__ == '__main__':
    board = _build_board()
    print(part1(board))
    print(part2(board))
