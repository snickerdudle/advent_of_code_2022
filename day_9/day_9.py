"""Day 9."""
from typing import Sequence, Union, Tuple
from collections import defaultdict, Counter
import re


dirs = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}


def get_data() -> Sequence[Sequence[Union[str, Sequence[str]]]]:
  with open('day_9.txt', 'r') as f:
    data = f.read().strip().split('\n')
    data = [i.split(' ') for i in data]
  return data


def need_to_move(head_pos: Tuple[int, int], tail_pos: Tuple[int, int]) -> bool:
  return not (
      abs(head_pos[0] - tail_pos[0]) <= 1
      and abs(head_pos[1] - tail_pos[1]) <= 1
  )


def get_new_pos(
    head_pos: Tuple[int, int], tail_pos: Tuple[int, int]
) -> Tuple[int, int]:
  if head_pos[0] == tail_pos[0]:
    # Check if simple right/left motion
    new_pos = (
        head_pos[0],
        (head_pos[1] + tail_pos[1]) // 2,
    )
  elif head_pos[1] == tail_pos[1]:
    # Check if simple up/down motion
    new_pos = (
        (head_pos[0] + tail_pos[0]) // 2,
        head_pos[1],
    )
  else:
    cur_r, cur_c = tail_pos
    if cur_r < head_pos[0]:
      cur_r += 1
    else:
      cur_r -= 1
    if cur_c < head_pos[1]:
      cur_c += 1
    else:
      cur_c -= 1
    new_pos = (
        cur_r,
        cur_c,
    )
  return new_pos


def part_1(len_of_unique=4) -> None:
  # First, get the data
  data = get_data()
  head_cell = (0, 0)
  tail_cell = (0, 0)
  visited = set([tail_cell])

  for motion in data:
    delta = dirs[motion[0]]
    for _ in range(int(motion[1])):
      head_cell = (head_cell[0] + delta[0], head_cell[1] + delta[1])
      if need_to_move(head_cell, tail_cell):
        tail_cell = get_new_pos(head_cell, tail_cell)
        visited.add(tail_cell)

  print(len(visited))


def part_2(num_links=1) -> None:
  # First, get the data
  data = get_data()
  head_cell = (0, 0)
  links = [(0, 0) for _ in range(num_links)]
  visited = set([(0, 0)])

  for motion in data:
    delta = dirs[motion[0]]
    for _ in range(int(motion[1])):
      head_cell = (head_cell[0] + delta[0], head_cell[1] + delta[1])

      cur_head = head_cell
      for link_idx in range(num_links):
        cur_tail = links[link_idx]
        if need_to_move(cur_head, cur_tail):
          new_tail_cell = get_new_pos(cur_head, cur_tail)
          links[link_idx] = new_tail_cell
          cur_head = new_tail_cell
        else:
          break
      visited.add(links[-1])

  print(len(visited))


if __name__ == '__main__':
  part_1()
  part_2(9)
