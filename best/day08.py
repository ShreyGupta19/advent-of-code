from utils import timed


def parse(file):
    with open(file) as f:
        return [[line[:3], int(line[4:])] for line in f]


def execute(insts):
    curr_inst = 0
    insts_called = set()
    accumulator = 0
    while curr_inst not in insts_called:
        if curr_inst >= len(insts):
            return accumulator, True
        inst, num = insts[curr_inst]
        insts_called.add(curr_inst)
        if inst == 'jmp':
            curr_inst += num
        elif inst == 'acc':
            accumulator += num
            curr_inst += 1
        elif inst == 'nop':
            curr_inst += 1
    return accumulator, False


@timed(8, 1)
def part_1(insts):
    """
    Since there's no conditionals in the instruction set, any loop in the program is an infinite
    loop. Hence, any time an instruction is called for the 2nd time, we know we're headed into an
    infinite loop. We can use a set to keep track of called instructions.
    """
    return execute(insts)[0]


@timed(8, 2)
def part_2(insts):
    """
    Absolute cake walk: just run our execute subroutine in a loop, switching one instruction at a
    time. As a small optimization, we skip the execute call when we see `acc` instructions.
    """
    inst_flip = {
        'jmp': 'nop',
        'nop': 'jmp'
    }
    for i, (inst, num) in enumerate(insts):
        if inst == 'acc':
            continue
        insts[i][0] = inst_flip[inst]
        acc, terminated = execute(insts)
        if terminated:
            return acc
        insts[i][0] = inst


if __name__ == '__main__':
    inputs = parse('../inputs/8.txt')
    part_1(inputs)
    part_2(inputs)
