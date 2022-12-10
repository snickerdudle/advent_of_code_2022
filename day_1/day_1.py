from typing import Sequence
import heapq


def get_data() -> Sequence[Sequence[str]]:
  with open('day_1.txt', 'r') as f:
    data = f.read().strip().split('\n\n')
    data = [i.strip().split('\n') for i in data]
  return data


def sum_of_calories(elf: Sequence[str]) -> int:
  return sum([int(i) for i in elf])


def part_1() -> None:
  # First, get the data
  data = get_data()
  h = []
  for elf in data:
    heapq.heappush(h, -sum_of_calories(elf))
  top_1 = 0
  for _ in range(1):
    top_1 += -heapq.heappop(h)
  return top_1


def part_2() -> None:
  # First, get the data
  data = get_data()
  h = []
  for elf in data:
    heapq.heappush(h, -sum_of_calories(elf))
  top_3 = 0
  for _ in range(3):
    top_3 += -heapq.heappop(h)
  return top_3


if __name__ == '__main__':
  print(part_1())
  print(part_2())
