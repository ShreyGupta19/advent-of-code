from advent import AdventProblem


def get_loop_num(target):
    val = 1
    i = 0
    while True:
        if target == val:
            return i
        val *= 7
        val %= 20201227
        i+=1

def part_1(keys):
    key_a, key_b = keys
    loops_a = get_loop_num(key_a)
    print
    # loops_b = get_loop_num(key_b)
    enc_key = 1
    for _ in range(loops_a):
        enc_key *= key_b
        enc_key %= 20201227
    return enc_key


def part_2(inputs):
    pass


if __name__ == '__main__':
    part1 = AdventProblem(25, 1, int)
    part1.add_solution(part_1)
    part1.run()

    # part2 = AdventProblem(3, 2, preprocess)
    # part2.add_solution(part_2)
    # part2.run()
