"""Day 4."""
from typing import Sequence, Union

priority = {}


def get_data() -> Sequence[Sequence[Union[str, Sequence[str]]]]:
  with open('day_4.txt', 'r') as f:
    data = f.read().strip().split('\n')
    for i, v in enumerate(data):
      l, r = v.strip().split(',')
      data[i] = sorted([
          tuple([int(ii) for ii in l.split('-')]),
          tuple([int(iii) for iii in r.split('-')]),
      ])
  return data


def a_fully_in_b(a: Sequence[int], b: Sequence[int]) -> bool:
  return a[0] >= b[0] and a[1] <= b[1]


def intersection_exists(a: Sequence[int], b: Sequence[int]) -> bool:
  set_a, set_b = set(i for i in range(a[0], a[1] + 1)), set(
      i for i in range(b[0], b[1] + 1)
  )
  return bool(set_a.intersection(set_b))


def part_1() -> None:
  # First, get the data
  data = get_data()
  total_score = 0
  for ls, rs in data:
    if a_fully_in_b(ls, rs) or a_fully_in_b(rs, ls):
      total_score += 1
  return total_score


def part_2() -> None:
  # First, get the data
  data = get_data()
  total_score = 0
  for ls, rs in data:
    if intersection_exists(ls, rs):
      total_score += 1
  return total_score


if __name__ == '__main__':
  print(part_1())
  print(part_2())
