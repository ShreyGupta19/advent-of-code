from advent import AdventProblem
import sys


def preprocess(lines):
    curr_player = None
    cards = [[], []]
    for line in lines:
        if line.startswith('Player 1:'):
            curr_player = 0
        elif line.startswith('Player 2:'):
            curr_player = 1
        elif len(line) > 0:
            cards[curr_player].append(int(line))
    return cards


def part_1(inputs):
    a_cards, b_cards = inputs
    total_cards = len(a_cards) + len(b_cards)
    while len(a_cards) < total_cards and len(b_cards) < total_cards:
        a_next = a_cards[0]
        b_next = b_cards[0]
        if a_next > b_next:
            a_cards += [a_next, b_next]
        elif a_next < b_next:
            b_cards += [b_next, a_next]
        else:
            print('same!')
        a_cards.pop(0)
        b_cards.pop(0)
    if len(a_cards) == total_cards:
        return sum(a * m for a, m in zip(a_cards, reversed(range(1, total_cards + 1))))
    if len(b_cards) == total_cards:
        return sum(b * m for b, m in zip(b_cards, reversed(range(1, total_cards + 1))))


def part_2(inputs):

    def play_round(a_cards, b_cards):
        total_cards = len(a_cards) + len(b_cards)
        seen = set()
        while len(a_cards) < total_cards and len(b_cards) < total_cards:
            state = (tuple(a_cards), tuple(b_cards))
            if state in seen:
                return True, False
            else:
                seen.add(state)
            a_next = a_cards[0]
            b_next = b_cards[0]
            a_cards.pop(0)
            b_cards.pop(0)
            if a_next > b_next and (a_next > len(a_cards) or b_next > len(b_cards)):
                a_cards += [a_next, b_next]
            elif a_next < b_next and (a_next > len(a_cards) or b_next > len(b_cards)):
                b_cards += [b_next, a_next]
            elif a_next <= len(a_cards) and b_next <= len(b_cards):
                a_won, b_won = play_round(a_cards.copy()[:a_next], b_cards.copy()[:b_next])
                if a_won:
                    a_cards += [a_next, b_next]
                elif b_won:
                    b_cards += [b_next, a_next]
        if len(a_cards) == total_cards:
            return True, False
        elif len(b_cards) == total_cards:
            return False, True

    a_cards, b_cards = inputs
    play_round(a_cards, b_cards)
    if a_cards:
        return sum(a * m for a, m in zip(a_cards, reversed(range(1, len(a_cards) + 1))))
    if b_cards:
        return sum(b * m for b, m in zip(b_cards, reversed(range(1, len(b_cards) + 1))))


if __name__ == '__main__':
    part1 = AdventProblem(22, 1, preprocess, 'file')
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(22, 2, preprocess, 'file')
    part2.add_solution(part_2)
    part2.run()
