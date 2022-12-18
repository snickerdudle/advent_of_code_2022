"""Day 18."""
from matplotlib import pyplot as plt
from queue import Queue


def get_data():
    with open('day_18.txt', 'r') as f:
        data = f.read().strip().split('\n')
        for i, v in enumerate(data):
            data[i] = [int(i) for i in v.strip().split(',')]
    return data


def AdjacentDirs(cur_cube=None):
    results = []
    for i in range(3):
        for d in [-1, 1]:
            cur_dir = [0, 0, 0] if cur_cube is None else list(cur_cube)
            cur_dir[i] = cur_dir[i] + d
            results.append(tuple(cur_dir))
    return results


def AddCoords(ca, cb):
    val = [ca[i] + cb[i] for i in range(len(ca))]
    if isinstance(ca, tuple):
        return tuple(val)
    return val


def CubeInBounds(cube, bounds):
    return all([bounds[i][0] <= cube[i] <= bounds[i][1] for i in range(3)])


def FloodFillCubes(
    bounds: list[list[int]], 
    real_cubes: dict[tuple, int], 
    ocean_cubes: dict[tuple, int]):
    q = Queue()
    # Queue the minimum number as the start cube
    start_cube = (bounds[0][0], bounds[1][0], bounds[2][0],)
    ocean_cubes[start_cube] = 6
    q.put(start_cube)

    while not q.empty():
        cur_cube = q.get()
        for new_cube in AdjacentDirs(cur_cube):
            if not CubeInBounds(new_cube, bounds):
                continue
            if new_cube in real_cubes:
                real_cubes[new_cube] += 1
                continue
            elif new_cube in ocean_cubes:
                continue
            else:
                ocean_cubes[new_cube] = 6
                q.put(new_cube)
    return

def FindSurfaceArea(all_cubes):
    for cube in all_cubes:
        for cur_cube in AdjacentDirs(cube):
            if cur_cube in all_cubes:
                all_cubes[cube] -= 1

    total_exposed_faces = sum(all_cubes.values())
    return total_exposed_faces


def part_1():
    data = get_data()
    # xs, ys, zs = zip(*data)
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(xs,ys,zs)
    # plt.show()

    all_cubes = {}
    for cube in data:
        all_cubes[tuple(cube)] = 6

    sa = FindSurfaceArea(all_cubes)
    print(sa)


def part_2():
    data = get_data()

    real_cubes = {}
    x_bounds = [float('inf'), float('-inf')]
    y_bounds = [float('inf'), float('-inf')]
    z_bounds = [float('inf'), float('-inf')]
    for cube in data:
        real_cubes[tuple(cube)] = 0
        x_bounds[0], x_bounds[1] = min(x_bounds[0], cube[0]), max(x_bounds[1], cube[0])
        y_bounds[0], y_bounds[1] = min(y_bounds[0], cube[1]), max(y_bounds[1], cube[1])
        z_bounds[0], z_bounds[1] = min(z_bounds[0], cube[2]), max(z_bounds[1], cube[2])

    # The bounds are inclusive
    x_bounds = [x_bounds[0] - 1, x_bounds[1] + 1]
    y_bounds = [y_bounds[0] - 1, y_bounds[1] + 1]
    z_bounds = [z_bounds[0] - 1, z_bounds[1] + 1]
    bounds = [x_bounds, y_bounds, z_bounds]

    # Now we have defined the bounds for the ocean, start recursively filling in
    # the ocean tiles
    ocean_cubes = {}
    FloodFillCubes(bounds, real_cubes, ocean_cubes)

    # Solution 1: the touched surfaces are marked as being outside
    print('Solution 1:', sum(real_cubes.values()))

    # Solution 2: the we calculate the entire surface area of ocean, and then
    # subtract the outside area
    sa = FindSurfaceArea(ocean_cubes)
    x = x_bounds[1] - x_bounds[0] + 1
    y = y_bounds[1] - y_bounds[0] + 1
    z = z_bounds[1] - z_bounds[0] + 1
    ocean_outer_surface = 2 * (x * y + x * z + y * z)

    print('Solution 2:', sa - ocean_outer_surface)






if __name__ == '__main__':
    part_1()
    part_2()
