import time


def timed(day_no, part_no):
    def timed_decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            ret = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f'DAY {day_no} PART {part_no}: {elapsed:.12f}s, RETURN = {ret}')
            return ret
        return wrapper
    return timed_decorator


def minmax(iterable):
    iterator = iter(iterable)
    min = next(iterator)
    max = min
    for i in iterator:
        if i < min:
            min = i
        elif i > max:
            max = i
    return min, max
