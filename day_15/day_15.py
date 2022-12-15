"""Day 15."""
import re
from tqdm import tqdm

target_y = 2_000_000
max_dim = 4_000_000


def get_data():
    with open('day_15.txt', 'r') as f:
        data = f.read().strip().split('\n')
        for i, v in enumerate(data):
            x_match = re.search(
                r'x=([\-\d]+).*y=([\-\d]+).*x=([\-\d]+).*y=([\-\d]+)', v)
            sensor_x, sensor_y, beacon_x, beacon_y = (
                x_match.group(1),
                x_match.group(2),
                x_match.group(3),
                x_match.group(4))
            data[i] = [
                [int(sensor_x), int(sensor_y)],
                [int(beacon_x), int(beacon_y)]]
        return data


def GetManhattanDistance(sensor, beacon):
    dist_x = abs(sensor[0] - beacon[0])
    dist_y = abs(sensor[1] - beacon[1])
    return dist_x + dist_y



def GetIntervalAtY(sensor: list[int], dist: int, y: int = target_y):
    # First check if any intersection at all.
    size_at_sensor = 1 + 2 * dist
    # Size decreases by 2 every row
    num_rows = abs(y - sensor[1])
    size_at_target = size_at_sensor - 2 * num_rows
    if size_at_target <= 0:
        return None
    ears = (size_at_target - 1) // 2

    interval = [sensor[0] - ears, sensor[0] + ears]

    return interval


def IsPointInIntervals(point, intervals, y=target_y):
    for i in intervals:
        if i[0] <= point[0] <= i[1] and point[1] == y:
            return True
    return False


def PrintAllIntervals(intervals):
    min_num, max_num = min(i[0] for i in intervals), max(i[1] for i in intervals)
    max_width = 60
    multiplier = max_width / (max_num - min_num)
    for l, r in intervals:
        left, right = l - min_num, max_num - r
        s = ' ' * int(left * multiplier)
        s += '#' * int((r-l) * multiplier)
        s += ' ' * int(right * multiplier)
        s += ' ' + str(l) + ',' + str(r)
        print(s)


def GetPossibleIntervalsFromData(data, all_points, y=target_y, trim=None):
    intervals = []

    for sensor, beacon in data:

        # Get the manhattan distance. This distance is inclusive (i.e if sensor
        # is at 5, and dist is 2, 3 and 7 are included)
        dist = GetManhattanDistance(sensor, beacon)

        # Now get the interval at target y
        interval = GetIntervalAtY(sensor, dist, y)
        if interval is not None:
            intervals.append(interval)

    # Now we sort the intervals
    intervals = sorted(intervals, key=lambda x: x[0])
    final_intervals = []
    for i in intervals:
        if not final_intervals:
            final_intervals.append(i)
        prev = final_intervals[-1]
        if i[0] <= prev[1]:
            # Merge
            final_intervals[-1] = [prev[0], max(i[1], prev[1])]
        else:
            final_intervals.append(i)

    if trim is not None:
        trimmed_intervals = []
        for interval in final_intervals:
            fit_x = trim[0] <= interval[0] <= trim[1]
            fit_y = trim[0] <= interval[1] <= trim[1]
            if fit_x and fit_y:
                trimmed_intervals.append(interval)
            else:
                if fit_x:
                    trimmed_intervals.append([interval[0], trim[1]])
                elif fit_y:
                    trimmed_intervals.append([trim[0], interval[1]])
                else:
                    if trim[0] > interval[0] and trim[1] < interval[1]:
                        trimmed_intervals.append(trim)
                    else:
                        continue
        return trimmed_intervals

    return final_intervals


def part_1():
    data = get_data()
    all_points = set([])
    for sensor, beacon in data:
        all_points.add(tuple(beacon))
        all_points.add(tuple(sensor))

    intervals = GetPossibleIntervalsFromData(data, all_points)

    final_num = 0
    for i in all_points:
        if IsPointInIntervals(i, intervals):
            final_num -= 1
    for i in intervals:
        final_num += i[1] - i[0] + 1

    print(final_num)
    return final_num


def part_2():
    data = get_data()
    all_points = set([])
    for sensor, beacon in data:
        all_points.add(tuple(beacon))
        all_points.add(tuple(sensor))

    possible_rows = {}

    # Perform the interval search for every row
    for row in tqdm(
        range(0, max_dim + 1),
        desc='Rows processed',
        unit='rows',
        miniters=50000,
        leave=False):
        intervals = GetPossibleIntervalsFromData(data, all_points, y=row, trim=[0, max_dim])
        if len(intervals) > 1:
            possible_rows[row] = intervals
    print(possible_rows)
    return possible_rows


if __name__ == '__main__':
    part_1()
    part_2()
