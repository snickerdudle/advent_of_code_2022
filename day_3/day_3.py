"""Day 3."""
from typing import Sequence, Union

priority = {}


def fill_in_priority():
  for i in range(ord('a'), ord('z') + 1):
    priority[chr(i)] = i - ord('a') + 1
  for i in range(ord('A'), ord('Z') + 1):
    priority[chr(i)] = i - ord('A') + 27


def get_data() -> Sequence[Sequence[Union[str, Sequence[str]]]]:
  with open('day_3.txt', 'r') as f:
    data = f.read().strip().split('\n')
    data = [i.strip() for i in data]
    for i, v in enumerate(data):
      data[i] = []
      data[i].append(v[:len(v)//2])
      data[i].append(v[len(v)//2:])
      data[i].append(set(data[i][0]))
      data[i].append(set(data[i][1]))
  return data


def part_1() -> None:
  # First, get the data
  data = get_data()
  total_score = 0
  for _, _, ls, rs in data:
    intersection = list(ls.intersection(rs))[0]
    total_score += priority[intersection]
  return total_score


def part_2() -> None:
  # First, get the data
  data = get_data()
  total_score = 0
  cur_idx = 0
  while cur_idx < len(data):
    elves = data[cur_idx:cur_idx + 3]
    elves = [i[2].union(i[3]) for i in elves]
    badge = list(elves[0].intersection(elves[1]).intersection(elves[2]))[0]
    total_score += priority[badge]
    cur_idx += 3
  return total_score


if __name__ == '__main__':
  fill_in_priority()
  # print(part_1())
  print(part_2())
