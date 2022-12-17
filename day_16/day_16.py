"""Day 16."""
import re
from queue import Queue
from functools import cache


class Valve:
    def __init__(self, name: str, rate: int=0):
        self.name = name
        self.rate = rate
        self.parents = []
        self.neighbors = []

    def UpdateRate(self, new_rate):
        self.rate = new_rate

    def AddNeighbor(self, neighbor):
        self.neighbors.append(neighbor)
        neighbor.parents.append(self)

    def __repr__(self):
        return f'<{self.name}({self.rate}): {[i.name for i in self.neighbors]}>'


def GetValve(name, all_valves):
    if name not in all_valves:
        all_valves[name] = Valve(name)

    return all_valves[name]


def get_data():
    all_valves = {}
    with open('day_16.txt', 'r') as f:
        data = f.read().strip().split('\n')
        for i, v in enumerate(data):
            cur_valve = re.match(r'Valve\s(\w+)', v).group(1)
            rate = int(re.search(r'rate=(\d+)', v).group(1))
            neighbors = [i.strip() for i in re.search(r'to\svalve[s]?\s(.+)', v).group(1).split(',')]
            
            cur_valve = GetValve(cur_valve, all_valves)
            cur_valve.UpdateRate(rate)
            for n in neighbors:
                n = GetValve(n, all_valves)
                cur_valve.AddNeighbor(n)

    return all_valves


def brute_force(start_valve, start_time_left=30):
    # Explore exhaustively through every node, return max flow gain from here.
    # Worst case performance is 5 ** 30 == 931322574615478515625 iterations
    q = Queue()
    opened = set()
    q.put((start_valve, start_time_left, opened, 0))

    max_flow = 0

    while not q.empty():
        cur_valve, time_left, opened, cur_max_flow = q.get()
        if time_left == 0:
            max_flow = max(max_flow, cur_max_flow)
            continue

        if cur_valve.rate and not cur_valve.name in opened:
            # One possibility is opening current valve. Try that and progress
            # from here
            new_opened = opened.copy()
            new_opened.add(cur_valve.name)
            for n in cur_valve.neighbors:
                q.put((n, time_left - 2, new_opened, cur_max_flow + cur_valve.rate))

        # Now try without actuating current valve
        for n in cur_valve.neighbors:
            q.put((n, time_left - 1, opened, cur_max_flow))

    return max_flow


@cache
def recursive_search(cur_valve, time_left=30, opened=None, allowed=None):
    # Memoize the max value achieved per time left
    total_released = 0
    opened = tuple() if opened is None else opened

    if time_left <= 0:
        return 0

    for n in cur_valve.neighbors:
        # First try to open and progress
        if cur_valve.rate and cur_valve.name not in opened:
            new_opened = tuple(sorted(opened + (cur_valve.name,)))
            total_released = max(total_released, (time_left - 1) * cur_valve.rate)
            if allowed is None or n.name in set(allowed):
                total_released = max(total_released, (time_left - 1) * cur_valve.rate + recursive_search(n, time_left - 2, new_opened, allowed))
        if allowed is None or n.name in set(allowed):
            # Now do the same without opening
            total_released = max(total_released, recursive_search(n, time_left - 1, opened, allowed))
    
    return total_released


def part_1():
    all_valves = get_data()
    cur_valve = GetValve('AA', all_valves)

    max_flow = recursive_search(cur_valve)
    print(max_flow)


def part_2():
    all_valves = get_data()
    cur_valve = GetValve('AA', all_valves)

    max_flow = recursive_search(cur_valve, allowed=tuple(i.name for i in all_valves.values()))
    print(max_flow)


if __name__ == '__main__':
    # part_1()
    part_2()