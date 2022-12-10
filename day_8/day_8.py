"""Day 8."""
from __future__ import annotations
from typing import Sequence, Optional, Any, Tuple
from collections import defaultdict, Counter


def get_data() -> Sequence[Sequence[int]]:
  with open('day_8.txt', 'r') as f:
    data = f.read().strip('').split('\n')
    data = [[int(c) for c in r] for r in data]
    return data


def get_visibility_mask(data):
  """Returns the highest trees seen at every point."""
  mask = [[True for c in range(len(data[0]))] for r in range(len(data))]

  # Start left-to-right
  for r in range(len(data)):
    cur_max = -float('inf')
    for c in range(len(data[r])):
      mask[r][c] = (data[r][c] <= cur_max) and mask[r][c]
      cur_max = max(cur_max, data[r][c])
  # Then right-to-left
  for r in range(len(data)):
    cur_max = -float('inf')
    for c in range(len(data[r]) - 1, -1, -1):
      mask[r][c] = (data[r][c] <= cur_max) and mask[r][c]
      cur_max = max(cur_max, data[r][c])
  # Up to down
  for c in range(len(data[0])):
    cur_max = -float('inf')
    for r in range(len(data)):
      mask[r][c] = (data[r][c] <= cur_max) and mask[r][c]
      cur_max = max(cur_max, data[r][c])
  # Then right-to-left
  for c in range(len(data[0])):
    cur_max = -float('inf')
    for r in range(len(data) - 1, -1, -1):
      mask[r][c] = (data[r][c] <= cur_max) and mask[r][c]
      cur_max = max(cur_max, data[r][c])
  return mask


def get_score(r, c, data):
  seen_trees = []

  # Check up
  cur = 0
  for rr in range(r - 1, -1, -1):
    cur += 1
    if data[rr][c] >= data[r][c]:
      break
  seen_trees.append(cur)
  # Check down
  cur = 0
  for rr in range(r + 1, len(data)):
    cur += 1
    if data[rr][c] >= data[r][c]:
      break
  seen_trees.append(cur)
  # Check left
  cur = 0
  for cc in range(c - 1, -1, -1):
    cur += 1
    if data[r][cc] >= data[r][c]:
      break
  seen_trees.append(cur)
  # Check right
  cur = 0
  for cc in range(c + 1, len(data[0])):
    cur += 1
    if data[r][cc] >= data[r][c]:
      break
  seen_trees.append(cur)
  
  result = 1
  for i in seen_trees:
    result *= i
  
  return result


def part_1():
  # First, get the data
  data = get_data()
  mask = get_visibility_mask(data)
  results = 0
  for i in mask:
    results += sum([not ii for ii in i])
  print(results)


def part_2():
  # First, get the data
  data = get_data()
  max_result = 0

  for r in range(len(data)):
    for c in range(len(data[r])):
      sc = get_score(r, c, data)
      max_result = max(max_result, sc)

  print(max_result)

if __name__ == '__main__':
  part_2()
