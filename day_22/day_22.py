"""Day 22."""
from __future__ import annotations
from typing import Union
dirs = {0: (0, 1,), 1: (1, 0,), 2: (0, -1,), 3: (-1, 0,)}


class Walker:
    def __init__(self, board: Board):
        self.board = board
        self.dir = 0  # right
        self.pos = self.GetStartPositionFromBoard()

    def GetStartPositionFromBoard(self):
        min_num, max_num = self.board.RowRange(1)
        for c in range(min_num, max_num + 1):
            if self.board.Get(1, c) == '.':
                return (1, c,)
        raise ValueError('Something wrong!')

    def Step(self, distance: int = 1):
        cur_pos = self.pos
        for step in range(distance):
            new_check = (cur_pos[0] + dirs[self.dir][0], cur_pos[1] + dirs[self.dir][1])
            # Justify depending on direction of motion
            if not self.dir % 2:
                # Right-left. Need to WrapRow
                new_check = self.board.WrapRow(*new_check)
            else:
                # Up-down. Need to WrapCol
                new_check = self.board.WrapCol(*new_check)
            new_tile = self.board.Get(*new_check)
            if new_tile == '.':
                cur_pos = new_check
            else:
                break
        self.pos = cur_pos
        return self.pos

    def Walk(self, directions: list[Union[str, int]]):
        for direction in directions:
            if direction == 'L':
                self.dir = (self.dir - 1) % 4
            elif direction == 'R':
                self.dir = (self.dir + 1) % 4
            else:
                self.Step(direction)
        print(self.pos)
        print(self.pos[0] * 1000 + self.pos[1] * 4 + self.dir)


class Board:
    def __init__(self, raw_board):
        self.raw_board = raw_board[:]
        self.row_minmax = self.AssignRowMinMaxFromRawBoard()
        self.col_minmax = self.AssignColMinMaxFromRawBoard()

    def AssignRowMinMaxFromRawBoard(self):
        row_minmax = {
            i + 1: [float('inf'), float('-inf')] for i in range(len(self.raw_board))}
        for r, row in enumerate(self.raw_board, start=1):
            for c in range(len(row)):
                col = row[c]
                if col != ' ':
                    row_minmax[r][0] = c + 1
                    break
            for c in range(len(row) - 1, -1, -1):
                col = row[c]
                if col != ' ':
                    row_minmax[r][1] = c + 1
                    break
        return row_minmax

    def AssignColMinMaxFromRawBoard(self):
        max_len = max(len(i) for i in self.raw_board)
        for r in range(len(self.raw_board)):
            self.raw_board[r] = self.raw_board[r].ljust(max_len, ' ')
        col_minmax = {
            i + 1: [float('inf'), float('-inf')] for i in range(max_len)}
        for c in range(max_len):
            for r in range(len(self.raw_board)):
                row = self.raw_board[r][c]
                if row != ' ':
                    col_minmax[c + 1][0] = r + 1
                    break
            for r in range(len(self.raw_board) - 1, -1, -1):
                row = self.raw_board[r][c]
                if row != ' ':
                    col_minmax[c + 1][1] = r + 1
                    break
        return col_minmax

    def RowRange(self, row: int):
        return self.row_minmax[row]

    def ColRange(self, col: int):
        return self.col_minmax[col]

    def WrapRow(self, row: int, col: int):
        """Returns row, COL."""
        row_min, row_max = self.RowRange(row)
        if row_min <= col <= row_max:
            return row, col

        # 5  6  7  8  9  10 11 12 13 14 ...
        #             5  6  7  8  5  6  ...
        col = (col - row_min) % (row_max - row_min + 1) + row_min
        return row, col

    def WrapCol(self, row: int, col: int):
        """Returns ROW, col."""
        col_min, col_max = self.ColRange(col)
        if col_min <= row <= col_max:
            return row, col

        # 5  6  7  8  9  10 11 12 13 14 ...
        #             5  6  7  8  5  6  ...
        row = (row - col_min) % (col_max - col_min + 1) + col_min
        return row, col

    def Get(self, row, col):
        return self.raw_board[row - 1][col - 1]

    def PrintBoard(self):
        print('\n'.join(self.raw_board))


def get_data():
    with open('day_22.txt', 'r') as f:
        board, directions = f.read().rstrip().split('\n\n')
        board = board.split('\n')
        b = Board(board)

    cur_idx = 0
    last_char = directions[0]
    results = []
    directions = directions + ' '
    for i in range(len(directions)):
        cur_char = directions[i]
        if cur_char.isnumeric() == last_char.isnumeric():
            continue
        else:
            # We are either on the cusp of num->letter or letter->num
            new_entry = directions[cur_idx:i]
            if new_entry.isnumeric():
                new_entry = int(new_entry)
            results.append(new_entry)
            cur_idx = i
        last_char = cur_char

    return b, results


def part_1():
    board, directions = get_data()
    walker = Walker(board)
    walker.Walk(directions)


def part_2():
    pass


if __name__ == '__main__':
    part_1()
    part_2()
