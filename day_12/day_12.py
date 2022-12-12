"""Day 12."""
from typing import Sequence, Union, Tuple, Callable
from queue import Queue


def chr_to_int(cur_char):
  result = ord(cur_char) - ord('a')
  if result < 0:
    return chr_to_int('z')
  return result



def get_data() -> Sequence[Sequence[int]]:
  with open('day_12.txt', 'r') as f:
    data = f.read().strip().split('\n')
    start = None
    end = None

    for i, v in enumerate(data):
      data[i] = []
      for ii, c in enumerate(v):
        if c == 'S':
          start = (i, ii,)
        elif c == 'E':
          end = (i, ii,)
        data[i].append(chr_to_int(c))

  return data, start, end


def GetNeighbors(data_map, cur_cell):
  neighbors = []
  cur_val = data_map[cur_cell[0]][cur_cell[1]]
  for d in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
    new_cell = (cur_cell[0] + d[0], cur_cell[1] + d[1],)
    if 0 <= new_cell[0] < len(data_map) and 0 <= new_cell[1] < len(data_map[0]):
      if data_map[new_cell[0]][new_cell[1]] <= cur_val + 1:
        neighbors.append(new_cell)
  return neighbors


def bfs(data_map, start, end, visited=None):
  if visited is None:
    visited = {}

  # Queue is filled with cell, path_to_cur_cell, prev_neighbor_dir
  q = Queue()
  q.put((start, 0,))
  while not q.empty():
    # While we have items in the queue, we first pop, check if 
    # already have them in visited
    # If not in visited, add its neighbors to queue
    # If visited, make sure to update with lowest
    cur_cell, cur_path_length = q.get()
    if cur_cell in visited:
      continue
    else:
      if cur_cell == end:
        return cur_path_length
      visited[cur_cell] = cur_path_length
      for neighbor in GetNeighbors(data_map, cur_cell):
        if neighbor not in visited:
          q.put((neighbor, cur_path_length + 1))

  return float('inf')



def part_1() -> None:
  # First, get the data
  data, start, end = get_data()
  print(bfs(data, start, end))

def part_2() -> None:
  # First, get the data
  data, start, end = get_data()

  start_positions = []
  for r in range(len(data)):
    for c in range(len(data[0])):
      if data[r][c] == 0:
        start_positions.append((r, c))
  
  min_length = float('inf')
  for i in start_positions:
    min_length = min(min_length, bfs(data, i, end))

  print(min_length)
  

if __name__ == '__main__':
  # part_1()
  part_2()
