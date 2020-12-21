from advent import AdventProblem


def preprocess(line):
    instruction = line[:3]
    number = int(line[4:])
    return [instruction, number]


def part_1(insts):
    not_called = set(range(len(insts)))
    curr_inst = 0
    accumulated = 0
    while curr_inst in not_called and curr_inst < len(insts):
        not_called.remove(curr_inst)
        inst = insts[curr_inst][0]
        if inst == 'nop':
            curr_inst += 1
        elif inst == 'acc':
            accumulated += insts[curr_inst][1]
            curr_inst += 1
        elif inst == 'jmp':
            curr_inst += insts[curr_inst][1]
    return accumulated, curr_inst == len(insts)

def part_2(insts):
    for i, (inst, num) in enumerate(insts):
        if inst == 'jmp':
            insts[i][0] = 'nop'
        elif inst == 'nop':
            insts[i][0] = 'jmp'
        acc, termed = part_1(insts)
        if termed:
            return acc
        if inst == 'jmp':
            insts[i][0] = 'jmp'
        elif inst == 'nop':
            insts[i][0] = 'nop'


if __name__ == '__main__':
    part1 = AdventProblem(8, 1, preprocess)
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(8, 2, preprocess)
    part2.add_solution(part_2)
    part2.run()
