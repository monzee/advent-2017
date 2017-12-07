from typing import Tuple
import re


def solve(initial: [int]) -> Tuple[int, int]:
    seen = {}
    arrangement = initial[:]
    size = len(arrangement)
    v = 0
    k = tuple(arrangement)
    while k not in seen:
        seen[k] = v
        v += 1
        n = max(arrangement)
        i = (arrangement.index(n) + 1) % size
        arrangement[i - 1] = 0
        for _ in range(n):
            arrangement[i] += 1
            i = (i + 1) % size
        k = tuple(arrangement)
    return len(seen), v - seen[k]


def parse(data_str: str) -> [int]:
    return [int(n) for n in re.split(r'\s+', data_str.strip())]


assert solve([0, 2, 7, 0]) == (5, 4)
print(solve(parse('4	1	15	12	0	9	9	5	5	8	7	3	14	5	12	3')))
