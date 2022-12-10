"""Day 7."""
from __future__ import annotations
from typing import Sequence, Optional, Any, Tuple
from collections import defaultdict, Counter
import re

_DIRECTORY = 0
_FILE = 1

class Node:
  def __init__(
      self,
      name: str,
      parent: Optional[Node] = None,
      size: Optional[int] = None,
  ) -> None:
    self.name = name
    self.parent = parent
    self.size = size
    self.kind = _DIRECTORY if self.size is None else _FILE
    self.level = self.parent.level + 1 if self.parent is not None else 0
    self.children = {}

  def PrintTree(self, return_string=False):
    s = self.level * '  ' + self.name + '\n'
    for _, child_node in self.children.items():
      s += child_node.PrintTree(True)

    if return_string:
      return s
    print(s)

  def AddChild(self, name: str, size_or_dir: str) -> Node:
    if name in self.children:
      return self.children[name]

    new_node = Node(
        name=name,
        parent=self,
        size=None if size_or_dir == 'dir' else int(size_or_dir),
    )
    self.children[name] = new_node
    return new_node

  def GetChild(self, name: str) -> Node:
    if name == '/':
      return root_node
    elif name == '..':
      return self.parent
    return self.children[name]

  def GetSize(self) -> int:
    if self.size is not None:
      return self.size
    else:
      size = 0
      for node in self.children.values():
        size += node.GetSize()
      self.size = size
      return size

  def GetAllDirs(self):
    if self.kind == _DIRECTORY:
      results = [self]
      for node in self.children.values():
        results += node.GetAllDirs()
      return results
    else:
      return []



root_node = Node('/')


def get_data() -> Sequence[Tuple[Sequence[str], Sequence[Sequence[str]]]]:
  with open('day_7.txt', 'r') as f:
    data = f.read().strip(' $').split('\n$ ')
    # Data is now a collection of commands and their outputs. Divide:
    output = []
    for _, v in enumerate(data):
      v = v.split('\n')
      command = v[0].strip().split(' ')
      command_results = [res.split(' ') for res in v[1:]]
      output.append((
          command,
          command_results,
      ))
  return output


def create_all_nodes(data):
  cur_node = root_node

  for input_part, results in data:
    command, args = input_part[0], input_part[1:]
    if command == 'cd':
      cur_node = cur_node.GetChild(args[0])
      continue
    elif command == 'ls':
      # Start creating all the files/dirs
      for size_or_dir, name in results:
        cur_node.AddChild(name, size_or_dir)


def part_1():
  # First, get the data
  data = get_data()
  
  create_all_nodes(data)
  root_node.GetSize()
  all_dirs = root_node.GetAllDirs()
  
  output = 0
  for d in all_dirs:
    if d.GetSize() <= 100_000:
      output += d.GetSize()
      
  return output
  
def part_2():
  fs_size = 70_000_000
  size_needed = 30_000_000
  cur_free = fs_size - root_node.GetSize()
  need_to_free_up = max(size_needed - cur_free, 0)
  print(need_to_free_up)
  
  all_dirs = root_node.GetAllDirs()
  all_dirs.sort(key=lambda d: d.GetSize())
  for d in all_dirs:
    if d.GetSize() >= need_to_free_up:
      # d.PrintTree()
      print(d.GetSize())
      break
      


if __name__ == '__main__':
  part_1()
  part_2()
