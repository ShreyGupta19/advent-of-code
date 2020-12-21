import re
from collections import defaultdict

from advent import AdventProblem

class Rule:
    def __init__(self, rm):
        self.field = rm.group(1)
        self.a = int(rm.group(2))
        self.b = int(rm.group(3))
        self.c = int(rm.group(4))
        self.d = int(rm.group(5))

    def __repr__(self):
        return f"{self.field}: {self.a} <= x <= {self.b} OR {self.c} <= x <= {self.d}"

    def __call__(self, value):
        return (self.a <= value <= self.b) or (self.c <= value <= self.d)


def preprocess(lines):
    i = 0
    rules = []
    while len(lines[i]) > 0:
        rm = re.match(r'([\w\s]+): (\d+)\-(\d+) or (\d+)\-(\d+)', lines[i])
        rules.append(Rule(rm))
        i += 1
    i += 2
    my_ticket = [int(x) for x in lines[i].split(',')]
    i += 3
    tickets = []
    while i < len(lines):
        tickets.append([int(x) for x in lines[i].split(',')])
        i += 1
    return rules, my_ticket, tickets


def part_1(inputs):
    rules, _, tickets = inputs
    bad_vals = []
    for ticket in tickets:
        for value in ticket:
            if not any(rule(value) for rule in rules):
                bad_vals.append(value)
                break
    return sum(bad_vals)

def part_2(inputs):
    rules, my_ticket, tickets = inputs
    good_tickets = []
    for ticket in tickets + [my_ticket]:
        bad_value_found = False
        for value in ticket:
            if not any(rule(value) for rule in rules):
                bad_value_found = True
                break
        if not bad_value_found:
            good_tickets.append(ticket)

    taken = set()
    field_mapping = defaultdict(list)
    for rule in rules:
        for slot in range(len(my_ticket)):
            if slot in taken:
                continue
            if all(rule(tx[slot]) for tx in good_tickets):
                field_mapping[rule.field].append(slot)
        if len(field_mapping[rule.field]) == 1:
            taken.add(slot)

    for k, v in field_mapping.items():
        print(k, v)

    # SOLVED BY HAND FROM HERE!

if __name__ == '__main__':
    part1 = AdventProblem(16, 1, preprocess, "file")
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(16, 2, preprocess, "file")
    part2.add_solution(part_2)
    part2.run()
