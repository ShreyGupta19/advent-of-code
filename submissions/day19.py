import re

from cachetools import cached
from cachetools.keys import hashkey

from advent import AdventProblem


def preprocess(lines):
    line_ctr = 0
    terms = {}
    non_terms = {}
    while len(lines[line_ctr]) > 0:
        rule_match = re.match(r'(\d+): (.+)', lines[line_ctr])
        rule_id = rule_match.group(1)
        rule_text = rule_match.group(2)
        if '"' in rule_text:
            terms[rule_id] = rule_text[1]
        else:
            options = rule_text.split('|')
            non_terms[rule_id] = [opt.split() for opt in options]
        line_ctr += 1

    inputs = [l.strip() for l in lines[line_ctr + 1:]]
    return terms, non_terms, inputs

@cached(cache={}, key=lambda rule, terms, non_terms, input, start, lv: hashkey(rule, input, start))
def check_match(rule, terms, non_terms, input, start, lv):
    if rule in terms:
        if input[start:].startswith(terms[rule]):
            return True, start + len(terms[rule])
        else:
            return False, None

    og_start = start
    if rule in non_terms:
        for opt in non_terms[rule]:
            failed = False
            for subrule in opt:
                valid, start = check_match(subrule, terms, non_terms, input, start, lv+1)
                if not valid:
                    failed = True
                    break
            if not failed:
                return True, start
            start = og_start
        return False, None

def part_1(inputs):
    terms, non_terms, inputs = inputs
    num = 0
    for input in inputs:
        valid, start = check_match('0', terms, non_terms, input, 0, 0)
        if valid and start == len(input):
            num += 1
    return num


if __name__ == '__main__':
    part1 = AdventProblem(19, 1, preprocess, 'file')
    part1.add_solution(part_1)
    part1.run()

    # PART 2 DOES NOT WORK YET.
    part2 = AdventProblem(19, 2, preprocess, 'file')
    part2.add_solution(part_1)
    part2.run()
