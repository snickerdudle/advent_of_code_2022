"""Day 9."""
from typing import Sequence, Union, Tuple
from collections import defaultdict, Counter
import re


def get_data() -> Sequence[Sequence[Union[str, Sequence[str]]]]:
  with open('day_10.txt', 'r') as f:
    data = f.read().strip().split('\n')
    data = [[i.split(' ')[0], i.split(' ')[1:]] for i in data]
  return data


checks = set([20, 60, 100, 140, 180, 220])

def part_1() -> None:
  # First, get the data
  data = get_data()
  
  cur_op_idx = 0
  cur_x_value = 1
  previous_op_trigger_cycle = 0

  cur_cycle = 0
  old_operation, old_value = 'noop', 0

  score = 0

  while cur_op_idx < len(data):

    if cur_cycle in checks:
      score += cur_cycle * cur_x_value

    if previous_op_trigger_cycle == cur_cycle:
      new_operation, new_value = data[cur_op_idx]
      if new_value:
        new_value = int(new_value[0])

      # If previous operation is addition, perform now
      if old_operation == 'noop':
        pass
      elif old_operation == 'addx':
        cur_x_value += old_value

      if new_operation == 'noop':
        previous_op_trigger_cycle = cur_cycle + 1
      elif new_operation == 'addx':
        previous_op_trigger_cycle = cur_cycle + 2

      old_operation, old_value = new_operation, new_value

      cur_op_idx += 1

    cur_cycle += 1

  print(score)


def part_2() -> None:
  # First, get the data
  data = get_data()
  
  cur_op_idx = 0
  cur_x_value = 1
  previous_op_trigger_cycle = 0

  cur_cycle = 0
  old_operation, old_value = 'noop', 0

  results = []

  while cur_op_idx < len(data):

    if cur_cycle > 0:
      conversion = (cur_cycle - 1) % 40 + 1
      if cur_x_value + 3 > conversion >= cur_x_value:
        results.append('X')
      else:
        results.append(' ')

    if previous_op_trigger_cycle == cur_cycle:
      new_operation, new_value = data[cur_op_idx]
      if new_value:
        new_value = int(new_value[0])

      # If previous operation is addition, perform now
      if old_operation == 'noop':
        pass
      elif old_operation == 'addx':
        cur_x_value += old_value

      if new_operation == 'noop':
        previous_op_trigger_cycle = cur_cycle + 1
      elif new_operation == 'addx':
        previous_op_trigger_cycle = cur_cycle + 2

      old_operation, old_value = new_operation, new_value

      cur_op_idx += 1

    cur_cycle += 1

  s = ''
  for i in range(6):
    s += ''.join(results[40*i:40*(i+1)]) + '\n'
  print(s)



if __name__ == '__main__':
  part_1()
  part_2()
