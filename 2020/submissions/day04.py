import re

from advent import AdventProblem


def preprocess(lines):
    passports = []
    current_passport = []
    for line in lines:
        if len(line) == 0:
            kv_strs = (" ".join(current_passport)).split(" ")
            passports.append(dict(kv_str.split(':') for kv_str in kv_strs))
            current_passport = []
        else:
            current_passport.append(line)
    return passports


def part_1(passports):
    REQUIRED_FIELDS = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
    valid = 0
    for passport in passports:
        if len(REQUIRED_FIELDS - set(passport.keys())) == 0:
            valid += 1
    return valid


def part_2(passports):
    REQUIRED_FIELDS = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
    valid = 0
    for passport in passports:
        if len(REQUIRED_FIELDS - set(passport.keys())) != 0:
            continue
        if not (1920 <= int(passport["byr"]) <= 2002):
            continue
        if not (2010 <= int(passport["iyr"]) <= 2020):
            continue
        if not (2020 <= int(passport["eyr"]) <= 2030):
            continue
        height_match = re.match(r'^(\d+)(in|cm)$', passport['hgt'])
        if not height_match:
            continue
        height_value = int(height_match.group(1))
        height_unit = height_match.group(2)
        if height_unit == 'cm' and not(150 <= height_value <= 193):
            continue
        if height_unit == 'in' and not(59 <= height_value <= 76):
            continue
        if not re.match(r'^#[a-f0-9]{6}$', passport["hcl"]):
            continue
        if passport["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            continue
        if not re.match(r'^[0-9]{9}$', passport["pid"]):
            continue
        valid += 1
    return valid


if __name__ == '__main__':
    part1 = AdventProblem(4, 1, preprocess, "file")
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(4, 2, preprocess, "file")
    part2.add_solution(part_2)
    part2.run()
