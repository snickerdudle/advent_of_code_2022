"""Day 14."""


def get_data():
    minx, miny = float('inf'), float('inf')
    maxx, maxy = float('-inf'), float('-inf')

    miny = 0

    with open('day_14.txt', 'r') as f:
        data_list = f.read().strip().split('\n')
        for i, line in enumerate(data_list):
            all_coords = line.strip().split(' -> ')
            all_coords = [[int(ii) for ii in c.split(',')] for c in all_coords]
            for c in all_coords:
                minx, miny = min(minx, c[0]), min(miny, c[1])
                maxx, maxy = max(maxx, c[0]), max(maxy, c[1])
            data_list[i] = all_coords

    return data_list, minx, maxx, miny, maxy


def MakeMapBlank(minx, maxx, miny, maxy):
    rows = maxy - miny + 1
    cols = maxx - minx + 1

    rock_map = [['.' for c in range(cols)] for r in range(rows)]
    return rock_map


def IsHorizontal(a_point, b_point):
    return a_point[1] == b_point[1]


def IsVertical(a_point, b_point):
    return a_point[0] == b_point[0]


def DrawWallOnMap(rock_map, s_point, e_point, minx, miny):
    # First check if horizontal
    if IsHorizontal(s_point, e_point):
        s, e = s_point[0], e_point[0]
        if e < s:
            # Always right to left
            s, e = e, s
        for c in range(s, e + 1):
            rock_map[s_point[1]-miny][c-minx] = '#'
    elif IsVertical(s_point, e_point):
        s, e = s_point[1], e_point[1]
        if e < s:
            # Always top to bottom
            s, e = e, s
        for r in range(s, e + 1):
            rock_map[r-miny][s_point[0]-minx] = '#'
    else:
        raise ValueError('The points are neither Hor nor Ver.')



def PopulateMap(rock_map, data, minx, miny):
    for path in data:
        for start_idx in range(len(path) - 1):
            s_point, e_point = path[start_idx], path[start_idx + 1]
            DrawWallOnMap(rock_map, s_point, e_point, minx, miny)
    return


def PrintedMap(rock_map, miny=0):
    s = ''
    for row in rock_map:
        s += str(miny).rjust(4) + ' '
        s += ''.join(row)
        s += '\n'
        miny += 1
    return s


def GetNextSandPos(rock_map, cur_pos):
    # Check if overflow
    next_row = cur_pos[1] + 1

    # First, check directly down
    if next_row >= len(rock_map):
        return None
    if rock_map[next_row][cur_pos[0]] == '.':
        # Free to move down
        return (cur_pos[0], next_row,)

    # Check if left is overflow
    if cur_pos[0] - 1 < 0:
        # Overflow achieved
        return None
    if rock_map[next_row][cur_pos[0] - 1] == '.':
        return (cur_pos[0] - 1, next_row)

    # Check if right is overflow
    if cur_pos[0] + 1 >= len(rock_map[0]):
        # Overflow achieved
        return None
    if rock_map[next_row][cur_pos[0] + 1] == '.':
        return (cur_pos[0] + 1, next_row)

    # If none of the above, we stay where we are
    return cur_pos


def SandCycle(rock_map, start_col, start_row):
    cur_pos = (start_col, start_row,)

    while True:
        next_pos = GetNextSandPos(rock_map, cur_pos)
        if next_pos is None:
            # Overflow achieved
            return True
        if next_pos == cur_pos:
            rock_map[cur_pos[1]][cur_pos[0]] = 'o'
            return False
        cur_pos = next_pos


def part_1():
    data, minx, maxx, miny, maxy = get_data()
    rock_map = MakeMapBlank(minx, maxx, miny, maxy)
    PopulateMap(rock_map, data, minx, miny)
    
    overflow_achieved = False
    counter = 0
    while not overflow_achieved:
        # Perform 1 cycle of sand falling
        overflow_achieved = SandCycle(rock_map, 500-minx, 0-miny)
        counter += 1

    print(PrintedMap(rock_map))

    print(counter - 1)
    

def part_2():
    pass


if __name__ == '__main__':
    part_1()
    part_2()
