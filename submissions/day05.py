from advent import AdventProblem


def convert_to_seat_id(seat):
    row = [0, 127]
    col = [0, 7]
    for letter in seat[:-3]:
        if letter == 'F':
            row[1] = (row[1] + row[0] - 1) // 2
        if letter == 'B':
            row[0] = (row[1] + row[0] + 1) // 2
    for letter in seat[-3:]:
        if letter == 'L':
            col[1] = (col[1] + col[0] - 1) // 2
        if letter == 'R':
            col[0] = (col[1] + col[0] + 1) // 2

    return row[0] * 8 + col[0]

def part_1(seats):
    return max(convert_to_seat_id(seat) for seat in seats)

def part_2(seats):
    seat_ids = sorted([convert_to_seat_id(seat) for seat in seats])
    for s1, s2 in zip(seat_ids[:-1], seat_ids[1:]):
        if s2 - s1 > 1:
            return s1 + 1


if __name__ == '__main__':
    part1 = AdventProblem(5, 1, lambda x: x)
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(5, 2, lambda x: x)
    part2.add_solution(part_2)
    part2.run()
