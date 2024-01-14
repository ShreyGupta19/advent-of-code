import copy

from advent import AdventProblem


def preprocess(lines):
    return [[ch for ch in line] for line in lines]

def part_1(state):
    def run_automata(state):
        new_state = copy.deepcopy(state)
        for r in range(len(state)):
            for c in range(len(state[r])):
                if state[r][c] == '.':
                    continue
                occupied = 0
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if not (i == 0 and j == 0) and (0 <= r + i < len(state)) and (0 <= c + j < len(state[0])) and state[r + i][c + j] == '#':
                            occupied += 1
                if occupied == 0 and state[r][c] == 'L':
                    new_state[r][c] = '#'
                if occupied >= 4 and state[r][c] == '#':
                    new_state[r][c] = 'L'
        return new_state
    curr_state = state
    while True:
        new_state = run_automata(curr_state)
        if new_state == curr_state:
            return sum(col == '#' for row in new_state for col in row)
        curr_state = new_state


def part_2(state):
    def count_occupied(state, r, c):
        occupied = 0
        for r_step in [-1, 0, 1]:
            for c_step in [-1, 0, 1]:
                if r_step == 0 and c_step == 0:
                    continue
                curr_r = r
                curr_c = c
                while True:
                    curr_r += r_step
                    curr_c += c_step
                    if curr_r < 0 or curr_r >= len(state):
                        break
                    if curr_c < 0 or curr_c >= len(state[0]):
                        break
                    if state[curr_r][curr_c] == '#':
                        occupied += 1
                    if state[curr_r][curr_c] != ".":
                        break
        return occupied

    def run_automata(state):
        new_state = copy.deepcopy(state)
        for r in range(len(state)):
            for c in range(len(state[r])):
                if state[r][c] == '.':
                    continue
                occupied = count_occupied(state, r, c)
                if occupied == 0 and state[r][c] == 'L':
                    new_state[r][c] = '#'
                if occupied >= 5 and state[r][c] == '#':
                    new_state[r][c] = 'L'
        return new_state

    curr_state = state
    while True:
        new_state = run_automata(curr_state)
        if new_state == curr_state:
            return sum(col == '#' for row in new_state for col in row)
        curr_state = new_state


if __name__ == '__main__':
    part1 = AdventProblem(11, 1, preprocess, "file")
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(11, 2, preprocess, "file")
    part2.add_solution(part_2)
    part2.run()
