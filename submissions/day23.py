from advent import AdventProblem

from tqdm import tqdm
from collections import deque

def preprocess(lines):
    return [int(x) for x in lines[0]]


def decrement_cup(n, wrap_to):
    if n == 1:
        return wrap_to
    else:
        return n - 1

def part_1(labelings):
    current_cup = labelings[0]
    order = labelings.copy()
    for _ in range(100):
        idx = order.index(current_cup)
        sidelined = [order[(idx + i) % len(order)] for i in range(1, 4)]
        for n in sidelined:
            order.remove(n)
        insert_cup = current_cup
        while insert_cup in sidelined or insert_cup == current_cup:
            insert_cup = decrement_cup(insert_cup, wrap_to=9)
        new_idx = order.index(insert_cup)
        order = order[:new_idx + 1] + sidelined + order[order.index(insert_cup) + 1:]
        current_cup = order[(order.index(current_cup) + 1) % len(order)]
    return order


class Node:
    def __init__(self, val, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

class CircularList:
    def __init__(self, elems):
        self.root = Node(None)
        prev = self.root
        self.indexer = {}
        for e in elems:
            new_node = Node(e, prev)
            self.indexer[e] = new_node
            prev.next = new_node
            prev = new_node
        prev.next = self.root.next
        self.root.next.prev = prev
        self.root = self.root.next
        self.len = len(elems)

    def __repr__(self):
        nxt = self.root
        elems = []
        for _ in range(self.len + 1):
            elems.append(nxt.val)
            nxt = nxt.next
        elems[-1] = str(elems[-1]) + ' (ROOT)'
        return str(elems)

    def delete_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        if node == self.root:
            self.root = node.next
        node.prev = None
        node.next = None
        self.len -= 1
        del self.indexer[node.val]
        return node.val

    def pop_slice(self, node, num):
        popped = []
        curr = node
        for _ in range(num):
            next_ = curr.next
            popped.append(self.delete_node(curr))
            curr = next_
        return popped

    def find(self, val):
        return self.indexer[val]

    def insert_slice(self, node, slice):
        slice.root.prev.next = node.next
        node.next.prev = slice.root.prev
        slice.root.prev = node
        node.next = slice.root
        self.len += slice.len
        self.indexer.update(slice.indexer)

def part_2(labelings):
    labelings = labelings + list(range(10, 1000000 + 1))
    order = CircularList(labelings)
    curr_node = order.root

    for _ in tqdm(range(10000000)):
        sidelined = order.pop_slice(curr_node.next, 3)
        dest_val = curr_node.val
        while dest_val in sidelined or dest_val == curr_node.val:
            dest_val = decrement_cup(dest_val, wrap_to=1000000)
        dest_node = order.find(dest_val)
        circular_slice = CircularList(sidelined)
        order.insert_slice(dest_node, circular_slice)
        curr_node = curr_node.next
    node_one = order.find(1)
    return node_one.next.val * node_one.next.next.val


if __name__ == '__main__':
    part1 = AdventProblem(23, 1, preprocess, 'file')
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(23, 2, preprocess, 'file')
    part2.add_solution(part_2)
    part2.run()
