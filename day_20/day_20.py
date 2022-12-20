"""Day 20."""
import time


class LinkedNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def AddRightNode(self, val):
        new_node = LinkedNode(val, left=self)
        self.right = new_node
        return new_node

    def InsertRightNode(self, right_node):
        old_right = self.right
        self.right = right_node
        right_node.right = old_right
        right_node.left = self
        if old_right is not None:
            old_right.left = right_node

    def AddLeftNode(self, val):
        new_node = LinkedNode(val, right=self)
        self.left = new_node
        return new_node

    def InsertLeftNode(self, left_node):
        old_left = self.left
        self.left = left_node
        left_node.left = old_left
        left_node.right = self
        if old_left is not None:
            old_left.right = left_node

    def CutOut(self):
        if self.left is not None:
            self.left.right = self.right
        if self.right is not None:
            self.right.left = self.left

    def MoveByVal(self, total_list_size=None):
        # Cut myself out
        cur_node = self
        move_val = abs(self.val)
        if total_list_size is not None and move_val:
            move_val =  move_val % (total_list_size - 1)

        if self.val > 0:
            self.CutOut()
            for _ in range(move_val):
                cur_node = cur_node.right
            cur_node.InsertRightNode(self)
        elif self.val < 0:
            self.CutOut()
            for _ in range(move_val):
                cur_node = cur_node.left
            cur_node.InsertLeftNode(self)
        else:
            pass

    def PrintChain(self):
        s = str(self)
        cur = self.right
        while cur is not self:
            s += str(cur)
            cur = cur.right
        print(s)

    def __repr__(self):
        return f'<{self.left.val if self.left is not None else "|"} {self.val} {self.right.val if self.right is not None else "|"}>'



def get_data():
    with open('day_20.txt', 'r') as f:
        data = f.read().strip().split()
        data = [int(i) for i in data]
    return data


def MakeLinkedListFromData(data):
    node_array = []
    head_node = LinkedNode(None)
    cur_node = head_node
    for v in data:
        cur_node = cur_node.AddRightNode(v)
        node_array.append(cur_node)
    head_node = head_node.right
    cur_node.right = head_node
    cur_node.right.left = cur_node
    return node_array


def part_1():
    data = get_data()
    node_array = MakeLinkedListFromData(data)
    zero_node = [i for i in node_array if i.val == 0][0]
    for node in node_array:
        node.MoveByVal()

    nums_to_search_for = {1000, 2000, 3000}
    cur = zero_node
    num = 0

    for i in range(1, max(nums_to_search_for) + 1):
        cur = cur.right
        if i in nums_to_search_for:
            num += cur.val

    print(num)


def part_2():
    data = get_data()
    data = [811589153 * i for i in data]
    node_array = MakeLinkedListFromData(data)
    zero_node = [i for i in node_array if i.val == 0][0]
    for repetition in range(10):
        for node in node_array:
            node.MoveByVal(len(node_array))

    nums_to_search_for = {1000, 2000, 3000}
    cur = zero_node
    num = 0

    for i in range(1, max(nums_to_search_for) + 1):
        cur = cur.right
        if i in nums_to_search_for:
            num += cur.val

    print(num)

if __name__ == '__main__':
    part_1()
    part_2()
