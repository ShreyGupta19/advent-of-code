import os
import time


INPUTS_DIR = os.path.join('..', 'inputs')


class AdventProblem:
    def __init__(self, day_number, part_number, preprocess_func, preprocess_scope="line"):
        self.day = day_number
        self.part = part_number
        self.preprocess = preprocess_func
        self.preprocess_scope = preprocess_scope

        self.input = os.path.join(INPUTS_DIR, f'{day_number}.txt')
        self.solutions = []

    def run(self):
        print(f'RUNNING DAY {self.day} PART {self.part}')
        with open(self.input) as f:
            if self.preprocess_scope == "line":
                data = [self.preprocess(l.strip()) for l in f]
            elif self.preprocess_scope == "file":
                data = self.preprocess([l.strip() for l in f])

        for i, solution in enumerate(self.solutions):
            start = time.time()
            res = solution(data)
            end = time.time()
            print(f'SOLUTION {i} ({end - start}s):\n{res}\n')

    def add_solution(self, solution):
        self.solutions.append(solution)
