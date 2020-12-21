from day01 import identify_sum_pair
from utils import minmax, timed


def parse(file):
    with open(file) as f:
        return [int(l.strip()) for l in f]



@timed(9, 1)
def part_1(nums):
    """
    We can reuse the hashset-based sum pair finder from Day 1 as a subroutine here. With a little
    bit of care, we can also maintain a sliding window set of 25 numbers in O(1) time.
    """
    window = set(nums[:25])
    for i in range(25, len(nums)):
        if identify_sum_pair(window, sum_to=nums[i]) is None:
            return nums[i]
        window.remove(nums[i - 25])
        window.add(nums[i])


@timed(9, 2)
def part_2(nums, target):
    """
    Since we're considering sums of *contiguous* ranges, there's only one correct decision to make
    given each number we encounter: if the sum is currently too large, get rid of the leftmost num,
    and if the sum is too small, add the next number.

    We use minmax to compute the min and max simultaneously, a small optimization that saves us an
    extra pass over the selected range.
    """
    left = 0
    right = 0
    contiguous_sum = nums[0]
    while contiguous_sum != target:
        if contiguous_sum > target:
            contiguous_sum -= nums[left]
            left += 1
        if contiguous_sum < target:
            right += 1
            contiguous_sum += nums[right]
    contiguous_range = nums[left:right+1]
    return sum(minmax(contiguous_range))


if __name__ == '__main__':
    inputs = parse('../inputs/9.txt')
    ret = part_1(inputs)
    part_2(inputs, ret)
