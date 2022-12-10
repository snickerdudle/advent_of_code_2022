"""Day 5."""
from typing import Sequence, Union
from collections import defaultdict
import re


def parse_crates(crates: str) -> dict[Sequence[str]]:
  crates = crates.split('\n')[::-1]
  num_cols = (len(crates[0]) + 1) // 4
  output = defaultdict(list)
  for i in range(1, len(crates)):
    for col in range(num_cols):
      if col >= len(crates[i]):
        break
      cur_text = crates[i][col * 4: (col + 1) * 4].strip('[] ')
      if cur_text:
        output[col + 1].append(cur_text)
  return output


def parse_operations(operations: str) -> dict[Sequence[str]]:
  operations = operations.strip().split('\n')
  output = []
  for operation in operations:
    m = re.match(r'move\s(\d+)\sfrom\s(\d+)\sto\s(\d+)', operation)
    output.append((int(m.group(1)), int(m.group(2)), int(m.group(3)),))
  return output


def get_data() -> Sequence[Sequence[Union[str, Sequence[str]]]]:
  with open('day_5.txt', 'r') as f:
    crates, operations = f.read().rstrip().split('\n\n')
    crates = parse_crates(crates)
    operations = parse_operations(operations)
  return crates, operations


def part_1() -> None:
  # First, get the data
  crates, operations = get_data()
  output = []

  for num, from_num, to_num in operations:
    for _ in range(num):
      crates[to_num].append(crates[from_num].pop())
  for i in range(len(crates)):
    output.append(crates[i + 1][-1])
  return ''.join(output)


def part_2() -> None:
  # First, get the data
  crates, operations = get_data()
  output = []

  for num, from_num, to_num in operations:
    cur_slice = crates[from_num][-num:]
    crates[from_num] = crates[from_num][:-num]
    crates[to_num] += cur_slice

  for i in range(len(crates)):
    output.append(crates[i + 1][-1])
  return ''.join(output)


if __name__ == '__main__':
  print(part_1())
  print(part_2())
