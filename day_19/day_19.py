"""Day 19."""
import re
from collections import defaultdict
from functools import cache
from tqdm import tqdm
import multiprocessing
import time


def get_data():
    with open('day_19.txt', 'r') as f:
        data = f.read().strip().split('\n')
    return data


def convert_data_to_blueprints(data):
    results = {}
    for i, v in enumerate(data):
        scan = re.search(r'Blueprint\s(\d+).*?'
            + r'Each\sore.*?(\d+)\sore.*?'
            + r'Each\sclay.*?(\d+)\sore.*?'
            + r'Each\sobsidian.*?(\d+)\sore.*?(\d+)\sclay.*?'
            + r'Each\sgeode.*?(\d+)\sore.*?(\d+)\sobsidian.*?',
            v)
        cur_id = int(scan.group(1))
        # Cost is (ore, clay, obsidian, geode)
        # Robots are (ore, clay, obsidian, geode)
        robot_cost = {r_idx:{s_idx: 0 for s_idx in range(4)} for r_idx in range(4)}
        # Ore
        robot_cost[0][0] = int(scan.group(2))
        # Clay
        robot_cost[1][0] = int(scan.group(3))
        # Obsidian
        robot_cost[2][0] = int(scan.group(4))
        robot_cost[2][1] = int(scan.group(5))
        # Geode
        robot_cost[3][1] = int(scan.group(6))
        robot_cost[3][2] = int(scan.group(7))

        results[cur_id] = robot_cost
    return results


def GetPossibleRobotsToBuild(blueprint, robots, stones):
    possible_idx = []
    for robot_idx in range(4):
        for stone_idx in range(4):
            if stones[stone_idx] < blueprint[robot_idx][stone_idx]:
                break
        else:
            possible_idx.append(robot_idx)
    return possible_idx


def BuildRobot(robot_idx, blueprint, stones):
    stones = list(stones)
    for stone_idx in range(4):
        stones[stone_idx] -= blueprint[robot_idx][stone_idx]
    return tuple(stones)


def HarvestAllRobots(robots, stones):
    stones = list(stones)
    for robot_idx, num_robots in enumerate(robots):
        stones[robot_idx] += num_robots
    return tuple(stones)


def RecursivelySearchMaxGeodes(blueprint_id, blueprint, max_reqs, cycles, robots, stones):
    max_geodes = stones[-1]
    if not cycles:
        return max_geodes

    # Try building a robot
    for robot_idx in GetPossibleRobotsToBuild(blueprint, robots, stones):
        # Check if we're at max required robot capacity
        if max_reqs[robot_idx] <= robots[robot_idx]:
            # If the maximum per-turn number of required stones is equal or is
            # less than the number of existing per-turn production units, prune
            # the tree here.
            continue
        new_stones = BuildRobot(robot_idx, blueprint, stones)
        # Harvest using existing robots
        new_stones = HarvestAllRobots(robots, new_stones)
        # Add the robot to the fleet
        new_robots = list(robots)
        new_robots[robot_idx] += 1
        new_robots = tuple(new_robots)
        max_geodes = max(max_geodes, RecursivelySearchMaxGeodes(blueprint_id, blueprint, max_reqs, cycles - 1, new_robots, new_stones))

    # Harvest using existing robots
    new_stones = HarvestAllRobots(robots, stones)
    max_geodes = max(max_geodes, RecursivelySearchMaxGeodes(blueprint_id, blueprint, max_reqs, cycles - 1, robots, new_stones))

    return max_geodes


def GetQualityLevel(q):
    data = q.get(block=True)
    blueprints = convert_data_to_blueprints(data)
    # Mapping from stone to max required number to make a robot
    max_reqs = {}

    for i, b in blueprints.items():
        # Update the maximum required stones
        max_reqs[i] = {s_idx: 0 for s_idx in range(4)}
        for robot_idx in range(4):
            for stone_idx in range(3):
                max_reqs[i][stone_idx] = max(max_reqs[i][stone_idx], b[robot_idx][stone_idx])
            max_reqs[i][3] = float('inf')

    # Ore, clay, obsidian, geode
    robots = (1, 0, 0, 0,)
    stones = (0, 0, 0, 0,)
    
    max_blueprint = None
    max_geodes = float('-inf')
    result = 0
    for blueprint_id, blueprint in blueprints.items():
        cur_geodes = RecursivelySearchMaxGeodes(
            blueprint_id,
            blueprint,
            max_reqs[blueprint_id],
            cycles = 24,
            robots = robots,
            stones = stones)
        if cur_geodes > max_geodes:
            max_blueprint = blueprint_id
            max_geodes = cur_geodes
        result += blueprint_id * cur_geodes
    print(blueprint_id, max_geodes, result)


def part_1():
    data = get_data()

    num_proc = min(int(multiprocessing.cpu_count() * 1.5), len(data))
    print(f'Using {num_proc} processes')
    procs = []

    multiprocessing.set_start_method('fork')

    for i in range(num_proc):
        q = multiprocessing.Queue()
        q.put([data[ii] for ii in range(len(data)) if ii % num_proc == i])
        procs.append(multiprocessing.Process(target=GetQualityLevel, args=(q,)))

    for p in procs:
        p.start()

    for i in procs:
        i.join()


def part_2():
    data = get_data()


if __name__ == '__main__':
    part_1()
    part_2()
