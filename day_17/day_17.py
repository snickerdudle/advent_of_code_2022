"""Day 17."""


RIGHT = True
LEFT = not RIGHT
BOARD_WIDTH = 7


class Wind:
    def __init__(self, dirs):
        self.dirs = dirs
        self.cur_point = 0

    def next(self):
        return_bool = self.dirs[self.cur_point]
        self.cur_point = (self.cur_point + 1) % len(self.dirs)
        return return_bool


class Board:
    def __init__(self, board_width = BOARD_WIDTH):
        self.board_width = board_width
        self.board = [['.' for _ in range(self.board_width)] for i in range(8)]

    def TryPush(
        self, 
        shape: list, 
        push_right: bool, 
        left_col: int, 
        top_row: int):
        self.MaybeExpandBoard(top_row)

        # Check for board boundary overflow
        shape_width = len(shape[0])
        if push_right:
            if left_col + shape_width == self.board_width:
                # At the very right already, return the same
                return left_col
        elif not push_right:
            if left_col == 0:
                return left_col

        # Now check for collisions
        for r, row in enumerate(shape[::-1]):
            for c, col in enumerate(row):
                cur_row = top_row - len(shape) + 1 + r
                cur_col = c + left_col
                if col == '.':
                    continue

                # Check what there is on the map to the right (or left) of us
                check_col = cur_col + (1 if push_right else -1)
                if self.board[cur_row][check_col] == '#':
                    return left_col

        return left_col + (1 if push_right else -1)

    def TryDrop(
        self, 
        shape: list, 
        left_col: int, 
        top_row: int):
        self.MaybeExpandBoard(top_row)

        # Check for collisions
        for r, row in enumerate(shape[::-1]):
            for c, col in enumerate(row):
                cur_row = top_row - len(shape) + 1 + r
                cur_col = c + left_col
                if col == '.':
                    continue

                # Check what there is on the map below us
                check_row = cur_row - 1
                if check_row < 0:
                    # Overflow, return current level
                    return top_row
                if self.board[check_row][cur_col] == '#':
                    return top_row

        return top_row - 1

    def Burn(
        self, 
        shape: list, 
        left_col: int, 
        top_row: int):

        for r, row in enumerate(shape[::-1]):
            for c, col in enumerate(row):
                cur_row = top_row - len(shape) + 1 + r
                cur_col = c + left_col
                if col == '.':
                    continue
                else:
                    self.board[cur_row][cur_col] = '#'
        return top_row


    def MaybeExpandBoard(self, top_row):
        if top_row >= len(self.board):
            # Double the size
            self.board = self.board + [['.' for _ in range(self.board_width)] for i in range(len(self.board))]
        return

    def PrintBoard(self, lowest_row=None):
        s = ['+' + '-' * self.board_width + '+']
        for i, line in enumerate(self.board):
            s.append('|' + ''.join(line) + '|')
            if lowest_row is not None and lowest_row == i:
                s[-1] += ' <<<<<'
        print('\n'.join(s[::-1]))



def get_data():
    """
    Returns a list of bools. If bool is True, pushes to the right. If False,
    pushes to the left.
    """
    with open('day_17.txt', 'r') as f:
        push_right = [i == '>' for i in list(f.read().strip())]
    wind = Wind(push_right)

    shapes = """####

            .#.
            ###
            .#.

            ..#
            ..#
            ###

            #
            #
            #
            #

            ##
            ##"""

    shapes = [i.strip() for i in shapes.split('\n\n')]
    for i, v in enumerate(shapes):
        v = [l.strip() for l in v.split('\n')]
        shapes[i] = v
    return wind, shapes


def part_1():
    wind, shapes = get_data()
    board = Board()
    highest_point = -1  # floor

    for shape_count in range(2022):
        # a = input('Press Enter')
        shape = shapes[shape_count % len(shapes)]
        lowest_row = highest_point + 3 + 1
        top_row = lowest_row + len(shape) - 1
        left_col = 2

        # Start the movement
        while True:
            # First, try moving
            left_col = board.TryPush(shape, wind.next(), left_col, top_row)
            # Now, try dropping
            new_top_row = board.TryDrop(shape, left_col, top_row)
            if new_top_row == top_row:
                # Firmly seated, burn onto map and conjure next shape
                highest_point = max(highest_point, board.Burn(shape, left_col, top_row))
                # board.PrintBoard(highest_point + 3 + 1)
                break
            top_row = new_top_row
    print(highest_point + 1)


def part_2():
    wind, shapes = get_data()
    board = Board()
    highest_point = -1  # floor
    all_its = []
    heights = []
    total_iterations = 1_000_000_000_000

    for shape_count in range(10_000):
        # a = input('Press Enter')
        shape = shapes[shape_count % len(shapes)]
        lowest_row = highest_point + 3 + 1
        top_row = lowest_row + len(shape) - 1
        left_col = 2
        its = 0

        # Start the movement
        while True:
            its += 1
            # First, try moving
            left_col = board.TryPush(shape, wind.next(), left_col, top_row)
            # Now, try dropping
            new_top_row = board.TryDrop(shape, left_col, top_row)
            if new_top_row == top_row:
                # Firmly seated, burn onto map and conjure next shape
                highest_point = max(highest_point, board.Burn(shape, left_col, top_row))
                heights.append(highest_point)
                # board.PrintBoard(highest_point + 3 + 1)
                all_its.append(its)
                break
            top_row = new_top_row
    # Find the frequency of repetition
    sample_segment = all_its[-100:]
    period = None
    for i in range(-100 - 1, -len(all_its) - 1, -1):
        if sample_segment == all_its[i:i+100]:
            period = -i - 100
            break
    if period is None:
        raise ValueError()

    # Start searching for the beginning of the repetition
    for i in range(len(all_its)):
        if all_its[i: i + period] == all_its[i + period: i + 2 * period]:
            repetition_start = i
            break

    # Find the height delta within the period
    height_start = heights[repetition_start - 1]
    height_delta = heights[repetition_start + period - 1] - heights[repetition_start - 1]
    # Find how many times the repetition takes place
    period_mod = (total_iterations - repetition_start) % period
    period_whole = (total_iterations - repetition_start) // period

    # Total height will be:
    # 1. the height of the first non-repeating section,
    # 2. a whole multiple of entire repeating sections
    # 3. and the first portion of the repeating section, only taking period_mod items
    total_height = height_start + height_delta * period_whole + (heights[repetition_start + period_mod - 1] - heights[repetition_start - 1]) + 1
    print(total_height)


if __name__ == '__main__':
    part_1()
    part_2()
