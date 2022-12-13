"""Day 13."""
import re
from typing import Optional


def get_data():
    with open('day_13.txt', 'r') as f:
        data_list = f.read().strip().split('\n\n')
    
    data = {}

    for i, v in enumerate(data_list):
        v = v.split('\n')
        data[i] = v

    return data


def ListNotation(inp_str: str):
    inp_str = re.sub(r'(\d+)', r'|\1|', inp_str)
    inp_str = re.sub(r'([\[\]])', r'|\1|', inp_str)
    inp_str = re.sub(r'[,\s]', r'', inp_str)
    inp_str = re.sub(r'[|]{2,}', r'|', inp_str).strip('|').split('|')
    return inp_str


class Node:
    def __init__(self, val:Optional[int]=None, parent=None):
        self.val = val
        self.parent = parent
        self.children = []
        self.mark = False

    def AddChild(self, child):
        self.children.append(child)
        child.parent = self

    def MakeIntoList(self):
        new_node = Node(self.val, self)
        self.children.append(new_node)
        self.val = None

    def IsList(self):
        return self.val is None

    def __le__(self, other):
        return self.LTE(other)

    def __ge__(self, other):
        return other.LTE(self)

    def __eq__(self, other):
        return self.Eq(other)

    def Eq(self, right_node):
        while True:
            if self.IsList():
                if not right_node.IsList():
                    right_node.MakeIntoList()
                if not (len(self.children) == len(right_node.children)):
                    return False
                for i, node in enumerate(self.children):
                    r_node = right_node.children[i]
                    if not node == r_node:
                        return False
            else:
                if right_node.IsList():
                    self.MakeIntoList()
                    continue
                else:
                    # L is num and R is num
                    return self.val == right_node.val
            return True

    def LTE(self, right_node):
        while True:
            if self.IsList():
                if not right_node.IsList():
                    right_node.MakeIntoList()
                for i, node in enumerate(self.children):
                    if i >= len(right_node.children):
                        return False
                    r_node = right_node.children[i]
                    lte, eq = node <= r_node, node == r_node
                    if not lte:
                        return False
                    if not eq:
                        return True
            else:
                if right_node.IsList():
                    self.MakeIntoList()
                    continue
                else:
                    # L is num and R is num
                    return self.val <= right_node.val
            return True

    def __repr__(self):
        return f'<{self.val}: {self.children}>'


def CreateNodesFromList(inp_list):
    # Construct the nodes
    cur_node = Node()
    cur_idx = 0

    while cur_idx < len(inp_list):
        cur_item = inp_list[cur_idx]
        if cur_item == '[':
            new_child = Node()
            cur_node.AddChild(new_child)
            cur_node = new_child
        elif cur_item == ']':
            cur_node = cur_node.parent
        else:
            # Deal with this as a number
            new_child = Node(val=int(cur_item), parent=cur_node)
            cur_node.AddChild(new_child)
        cur_idx += 1

    return cur_node


def bubble_sort(nums):
    keep_going = True
    while keep_going:
        keep_going = False
        for i in range(len(nums) - 1):
            if nums[i + 1] <= nums[i] :
                # Swap the elements
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                # Set the flag to True so we'll loop again
                keep_going = True



def part_1():
    data = get_data()
    correct_idx = []

    for i in range(len(data)):
        l, r = data[i]
        l, r = ListNotation(l), ListNotation(r)
        
        l_node = CreateNodesFromList(l)
        r_node = CreateNodesFromList(r)

        if l_node.LTE(r_node):
            correct_idx.append(i + 1)
    print(correct_idx)
    print(sum(correct_idx))


def part_2():
    additional_packets = ['[[2]]','[[6]]']
    data = get_data()
    data[len(data)] = additional_packets
    packets = []

    for i in range(len(data)):
        l, r = data[i]
        l, r = ListNotation(l), ListNotation(r)
        
        l_node = CreateNodesFromList(l)
        r_node = CreateNodesFromList(r)

        packets.append(l_node)
        packets.append(r_node)

    packets[-2].mark = True
    packets[-1].mark = True

    bubble_sort(packets)

    a = 1
    for i, p in enumerate(packets):
        if p.mark:
            a *= (i + 1)
    print(a)


if __name__ == '__main__':
    part_1()
    part_2()
