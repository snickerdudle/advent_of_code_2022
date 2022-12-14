"""Day 6."""
from typing import Sequence, Union
from collections import Counter
import re


def get_data() -> Sequence[Sequence[Union[str, Sequence[str]]]]:
  with open('day_6.txt', 'r') as f:
    data = f.read().strip()
  return data


def part_1(len_of_unique=4) -> None:
  # First, get the data
  data = get_data()
  output = len_of_unique
  char_set = Counter(data[:len_of_unique])
  if len(char_set) == len_of_unique:
    return output

  while output < len(data):
    output += 1
    new_char = data[output - 1]
    old_char = data[output - 1 - len_of_unique]
    char_set.update([new_char])
    char_set.subtract([old_char])
    if char_set[old_char] == 0:
      del char_set[old_char]

    if len(char_set) == len_of_unique:
      return output


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
  print(part_1(14))
  # print(part_2())
