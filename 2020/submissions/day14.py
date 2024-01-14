import itertools
import re

from advent import AdventProblem


def preprocess_part_1(lines):
    mem_insts = []
    for l in lines:
        mask_match = re.match(r'mask = ([X10]{36})', l)
        if mask_match:
            ones_mask = int(mask_match.group(1).replace('X', '0'), 2)
            zeros_mask = int(mask_match.group(1).replace('X', '1'), 2)
            mem_insts.append((zeros_mask, ones_mask, []))
        else:
            mem_match = re.match(r'mem\[(\d+)\] = (\d+)', l)
            mem_insts[-1][-1].append((int(mem_match.group(1)), int(mem_match.group(2))))
    return mem_insts

def part_1(mem_insts):
    mem = {}
    for zeros_mask, ones_mask, insts in mem_insts:
        for inst in insts:
            mem[inst[0]] = (inst[1] | ones_mask) & zeros_mask
    return sum(mem.values())

def preprocess_part_2(lines):
    mem_insts = []
    for l in lines:
        mask_match = re.match(r'mask = ([X10]{36})', l)
        if mask_match:
            mem_insts.append((mask_match.group(1), []))
        else:
            mem_match = re.match(r'mem\[(\d+)\] = (\d+)', l)
            mem_insts[-1][-1].append((int(mem_match.group(1)), int(mem_match.group(2))))
    return mem_insts

def part_2(mem_insts):
    mem = {}
    for mask, insts in mem_insts:
        for inst in insts:
            mem_addr, val = inst
            mem_addr = list("{:036b}".format(mem_addr))
            for i, ch in enumerate(mask):
                if ch in ['1', 'X']:
                    mem_addr[i] = ch
            mem_addr = ''.join((mem_addr))
            for assigns in itertools.product(*[('0', '1') for _ in range(mask.count('X'))]):
                mem_split = mem_addr.split('X')
                new_addr = ''.join(itertools.chain(*zip(mem_split, assigns))) + mem_split[-1]
                mem[new_addr] = val
    return sum(mem.values())



if __name__ == '__main__':
    part1 = AdventProblem(14, 1, preprocess_part_1, 'file')
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(14, 2, preprocess_part_2, 'file')
    part2.add_solution(part_2)
    part2.run()
