import itertools

from advent import AdventProblem


def preprocess_part_1(lines):
    grid = set()
    for x, line in enumerate(lines):
        for y, ch in enumerate(line):
            if ch == '#':
                grid.add((x, y, 0))
    return grid


def preprocess_part_2(lines):
    grid = set()
    for x, line in enumerate(lines):
        for y, ch in enumerate(line):
            if ch == '#':
                grid.add((x, y, 0, 0))
    return grid

def part_1(grid):
    def get_neighbors(pos):
        neighbors = []
        for indices in itertools.chain(itertools.combinations(range(3), 1), itertools.combinations(range(3), 2), itertools.combinations(range(3), 3)):
            for deltas in itertools.product(*[[-1, 1] for _ in range(len(indices))]):
                new_pos = list(pos)
                for i in range(len(indices)):
                    new_pos[indices[i]] += deltas[i]
                neighbors.append(tuple(new_pos))
        return neighbors

    def get_coord_range(actives, i):
        return min(actives, key=lambda x: x[i])[i], max(actives, key=lambda x: x[i])[i]

    for cycle in range(6):
        new_grid = set()
        x_min, x_max = get_coord_range(grid, 0)
        y_min, y_max = get_coord_range(grid, 1)
        z_min, z_max = get_coord_range(grid, 2)
        for i, j, k in itertools.product(range(x_min - 1, x_max + 2), range(y_min - 1, y_max + 2), range(z_min - 1, z_max + 2)):
            pos = (i, j, k)
            active = pos in grid
            active_count = 0
            actives_found = []
            for n in get_neighbors(pos):
                active_count += (n in grid)
                if n in grid:
                    actives_found.append(n)
            if active and active_count in [2, 3]:
                new_grid.add(pos)
            elif not active and active_count == 3:
                new_grid.add(pos)
        grid = new_grid
    return len(new_grid)


def part_2(grid):
    def get_neighbors(pos):
        neighbors = []
        for indices in itertools.chain(itertools.combinations(range(4), 1), itertools.combinations(range(4), 2), itertools.combinations(range(4), 3), itertools.combinations(range(4), 4)):
            for deltas in itertools.product(*[[-1, 1] for _ in range(len(indices))]):
                new_pos = list(pos)
                for i in range(len(indices)):
                    new_pos[indices[i]] += deltas[i]
                neighbors.append(tuple(new_pos))
        return neighbors

    def get_coord_range(actives, i):
        return min(actives, key=lambda x: x[i])[i], max(actives, key=lambda x: x[i])[i]

    for cycle in range(6):
        new_grid = set()
        x_min, x_max = get_coord_range(grid, 0)
        y_min, y_max = get_coord_range(grid, 1)
        z_min, z_max = get_coord_range(grid, 2)
        w_min, w_max = get_coord_range(grid, 3)
        for i, j, k, l in itertools.product(range(x_min - 1, x_max + 2), range(y_min - 1, y_max + 2), range(z_min - 1, z_max + 2), range(w_min - 1, w_max + 2)):
            pos = (i, j, k, l)
            active = pos in grid
            active_count = 0
            actives_found = []
            for n in get_neighbors(pos):
                active_count += (n in grid)
                if n in grid:
                    actives_found.append(n)
            if active and active_count in [2, 3]:
                new_grid.add(pos)
            elif not active and active_count == 3:
                new_grid.add(pos)
        grid = new_grid
    return len(new_grid)


if __name__ == '__main__':
    part1 = AdventProblem(17, 1, preprocess_part_1, 'file')
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(17, 2, preprocess_part_2, 'file')
    part2.add_solution(part_2)
    part2.run()
