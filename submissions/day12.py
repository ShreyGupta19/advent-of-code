from advent import AdventProblem


def preprocess(line):
    return line[0], int(line[1:])


def step_in_dir(pos, dir, steps):
    new_pos = list(pos)
    if dir == 'N':
        new_pos[1] += steps
    if dir == 'S':
        new_pos[1] -= steps
    if dir == 'E':
        new_pos[0] += steps
    if dir == 'W':
        new_pos[0] -= steps
    return new_pos

def part_1(instrs):
    dirs = ['E', 'N', 'W', 'S']
    reversed_dirs = list(reversed(dirs))
    curr_dir = 'E'
    pos = (0, 0)
    for instr, steps in instrs:
        if instr in dirs:
            pos = step_in_dir(pos, instr, steps)
        elif instr == 'F':
            pos = step_in_dir(pos, curr_dir, steps)
        elif instr == 'L':
            curr_dir = dirs[(steps // 90 + dirs.index(curr_dir)) % len(dirs)]
        elif instr == 'R':
            curr_dir = reversed_dirs[(steps // 90 + reversed_dirs.index(curr_dir)) % len(reversed_dirs)]
    return abs(pos[1]) + abs(pos[0])

def move_left(waypoint_pos, degs):
    if degs == 90:
        waypoint_pos = (-waypoint_pos[1], waypoint_pos[0])
    if degs == 180:
        waypoint_pos = (-waypoint_pos[0], -waypoint_pos[1])
    if degs == 270:
        waypoint_pos = (waypoint_pos[1], -waypoint_pos[0])
    return waypoint_pos


def part_2(instrs):
    dirs = ['E', 'N', 'W', 'S']
    reversed_dirs = list(reversed(dirs))
    pos = [0, 0]
    waypoint_pos = [10, 1]
    for instr, steps in instrs:
        if instr in dirs:
            waypoint_pos = step_in_dir(waypoint_pos, instr, steps)
        elif instr == 'F':
            pos[0] += waypoint_pos[0] * steps
            pos[1] += waypoint_pos[1] * steps
        elif instr == 'L':
            waypoint_pos = move_left(waypoint_pos, steps)
        elif instr == 'R':
            waypoint_pos = move_left(waypoint_pos, 360 - steps)
    return abs(pos[1]) + abs(pos[0])


if __name__ == '__main__':
    part1 = AdventProblem(12, 1, preprocess)
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(12, 2, preprocess)
    part2.add_solution(part_2)
    part2.run()
