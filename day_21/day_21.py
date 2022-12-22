"""Day 21."""


mapping = {
    '+': int.__add__,
    '-': int.__sub__,
    '*': int.__mul__,
    '/': int.__truediv__
    }


def get_data():
    with open('day_21.txt', 'r') as f:
        data = f.read().strip().split('\n')
        results = {}
        for i, v in enumerate(data):
            name, operation = [i.strip() for i in v.split(':')]
            if operation.isnumeric():
                operation = int(operation)
            else:
                operation = operation.split(' ')
                operation = (operation[1], (operation[0], operation[2],),)
            results[name] = operation
    return results


def GetValueOfName(name, raw_data, computed):
    if name not in computed:
        operation = raw_data[name]
        if isinstance(operation, int):
            computed[name] = operation
        else:
            sign, [a, b] = operation
            result = int(mapping[sign](
                GetValueOfName(a, raw_data, computed),
                GetValueOfName(b, raw_data, computed)))
            computed[name] = result

    return computed[name]


def part_1():
    data = get_data()
    computed = {}
    result = GetValueOfName('root', data, computed)
    print(result)


def part_2():
    pass


if __name__ == '__main__':
    part_1()
    part_2()
