import re
from collections import Counter, defaultdict

from advent import AdventProblem


def preprocess(line):
    match = re.match(r'([\w\s]+)(\(contains [\w\,\s]+\))?', line)
    ingredients = match.group(1).split()
    if match.group(2) is not None:
        allergens = match.group(2)[len('(contains '):-1].split(', ')
    else:
        allergens = None
    return ingredients, allergens

def part_1(inputs):
    def get_options(inputs):
        allergen_counts = defaultdict(lambda: [defaultdict(int), 0])
        for input in inputs:
            ingredients, allergens = input
            if allergens is None:
                continue
            for allergen in allergens:
                for ingredient in ingredients:
                    allergen_counts[allergen][0][ingredient] += 1
                allergen_counts[allergen][1] += 1

        allergen_options = defaultdict(list)
        for allergen, (ingredient_counts, num_occur) in allergen_counts.items():
            for i, c in ingredient_counts.items():
                if c == num_occur:
                    allergen_options[allergen].append(i)

        return allergen_options

    options = get_options(inputs)
    all_ingredients = []
    for ingredients, _ in inputs:
        all_ingredients.extend(ingredients)
    all_suspects = []
    for ingredients in options.values():
        all_suspects += ingredients
    total = 0
    for i, c in Counter(all_ingredients).items():
        if i not in all_suspects:
            total += c
    return total


def part_2(inputs):
    def get_options(inputs):
        allergen_counts = defaultdict(lambda: [defaultdict(int), 0])
        for input in inputs:
            ingredients, allergens = input
            if allergens is None:
                continue
            for allergen in allergens:
                for ingredient in ingredients:
                    allergen_counts[allergen][0][ingredient] += 1
                allergen_counts[allergen][1] += 1

        allergen_options = defaultdict(list)
        for allergen, (ingredient_counts, num_occur) in allergen_counts.items():
            for i, c in ingredient_counts.items():
                if c == num_occur:
                    allergen_options[allergen].append(i)

        return allergen_options

    options = get_options(inputs)
    definite_mapping = {}
    while any(len(v) == 1 for v in options.values()):
        allergen, ingredients = next((k, v) for k, v in options.items() if len(v) == 1)
        del options[allergen]
        definite_mapping[allergen] = ingredients[0]
        for v in options.values():
            if ingredients[0] in v:
                v.remove(ingredients[0])

    return ','.join([v for _, v in sorted(definite_mapping.items())])

if __name__ == '__main__':
    part1 = AdventProblem(21, 1, preprocess)
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(21, 2, preprocess)
    part2.add_solution(part_2)
    part2.run()
