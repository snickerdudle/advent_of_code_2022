"""Day 11."""
from typing import Sequence, Union, Tuple, Callable
from collections import defaultdict, Counter
import re
from queue import Queue


monkeys = {}
global_mods = []


class RichNumber:
  def __init__(self, val, mods: list[int]):
    self.mods = mods
    self.start_val = val
    self.vals = self.CraeteValsFromValue()
    print(self.start_val, self.vals)

  def CraeteValsFromValue(self) -> dict[int, int]:
    vals = {}
    for i, m in enumerate(self.mods):
      vals[i] = self.start_val % m

    return vals

  def AddNum(self, new_num):
    for i in range(len(self.vals)):
      self.vals[i] = (self.vals[i] + new_num) % self.mods[i]

  def MulNum(self, new_num):
    for i in range(len(self.vals)):
      if isinstance(new_num, RichNumber):
        self.vals[i] *= self.vals[i]
        self.vals[i] %= self.mods[i]
      else:
        self.vals[i] = (self.vals[i] * new_num) % self.mods[i]

  def IsDivisibleByMonkeyIdx(self, monkey_idx):
    return not self.vals[monkey_idx]


class Monkey:
  def __init__(self, id: int, operation: list, div_num: int, id_true: int, id_false: int):
    self.id = id
    self.operation = operation
    self.div_num = div_num
    self.id_true = id_true
    self.id_false = id_false
    self.objects = Queue()
    self.num_objects_handled = 0

  def AssignObjects(self, objects):
    for i in objects:
      cur_num = RichNumber(i, global_mods)
      self.objects.put(cur_num)

  def ReceiveObject(self, new_object: RichNumber):
    self.objects.put(new_object)

  def RetrieveObject(self):
    if self.HasObjects():
      return self.objects.get()

  def HasObjects(self):
    return not self.objects.empty()

  def TriageTopObject(self, divide_by_3):
    # First, increase interest
    cur_object = self.RetrieveObject()
    if self.operation[1].isnumeric():
      num = int(self.operation[1])
    else:
      num = cur_object
    if self.operation[0] == '+':
      cur_object.AddNum(num)
    else:
      cur_object.MulNum(num)      

    # Decide if it matches the test_func
    if cur_object.IsDivisibleByMonkeyIdx(self.id):
      monkeys[self.id_true].ReceiveObject(cur_object)
    else:
      monkeys[self.id_false].ReceiveObject(cur_object)

    self.num_objects_handled += 1

  def DealWithAllObjects(self, divide_by_3):
    while self.HasObjects():
      self.TriageTopObject(divide_by_3)


def get_data() -> Sequence[Sequence[Union[str, Sequence[str]]]]:
  with open('day_11.txt', 'r') as f:
    data = f.read().strip().split('\n\n')
    for i, v in enumerate(data):
      div_num = int(re.search(r'divisible\sby\s(\d+)', v).group(1))
      global_mods.append(div_num)

    for i, v in enumerate(data):
      cur_id = int(re.search(r'Monkey\s(\d+)', v).group(1))
      objects = re.search(r'Starting\sitems:\s([\d,\s]+)', v).group(1)
      objects = re.sub(',', '', objects)
      objects = [int(i) for i in objects.strip().split(' ')]
      
      operation = re.search(r'new = old (.)\s([\d\w]{1,3})', v)
      operation = [operation.group(1), operation.group(2)]

      id_true = int(re.search(r'If\strue:\sthrow\sto\smonkey\s(\d+)', v).group(1))
      id_false = int(re.search(r'If\sfalse:\sthrow\sto\smonkey\s(\d+)', v).group(1))
      
      monkey = Monkey(id=cur_id, operation=operation, div_num=div_num, id_true=id_true, id_false=id_false)
      monkey.AssignObjects(objects)
      monkeys[cur_id] = monkey

  return data


def part_1(num_rounds, divide_by_3=True) -> None:
  # First, get the data
  data = get_data()

  for round_num in range(num_rounds):
    for i in range(len(monkeys)):
      monkeys[i].DealWithAllObjects(divide_by_3)


  handled = sorted(monkeys.values(), key=lambda x: x.num_objects_handled, reverse=True)
  print(handled)
  print(handled[0].num_objects_handled * handled[1].num_objects_handled)


if __name__ == '__main__':
  part_1(10000, divide_by_3=False)
  # part_2()
