from typing import List, TypeVar
from functools import reduce

T = TypeVar('T')


def solve(elems: List[int], lengths: List[int]) -> int:
    sparse_hash(elems, lengths, 1)
    return elems[0] * elems[1]


def solve2(lengths: List[int]) -> str:
    elems = list(range(256))
    sparse_hash(elems, lengths, 64)
    return ('{:02x}'*16).format(*dense_hash(elems))


def dense_hash(elems: List[int]):
    blocks = [elems[i*16:(i + 1)*16] for i in range(16)]
    return [reduce(lambda x, y: x ^ y, block, 0) for block in blocks]


def sparse_hash(elems: List[int], lengths: List[int], rounds: int = 1):
    pos = 0
    skip = 0
    n = len(elems)
    for _ in range(rounds):
        for l in lengths:
            reverse(elems, pos, l)
            pos = (pos + l + skip) % n
            skip += 1


def reverse(items: List[T], start: int, count: int):
    n = len(items)
    end = (start + count) % n
    if start <= end:
        for i, e in enumerate(items[start:end]):
            items[end - i - 1] = e
    else:
        sub = items[start:] + items[:end]
        for i, e in enumerate(sub[::-1]):
            items[(start + i) % n] = e


def to_lengths(s: str) -> List[int]:
    return [ord(c) for c in s] + [17, 31, 73, 47, 23]


assert solve([0, 1, 2, 3, 4], [3, 4, 1, 5]) == 12
data = '14,58,0,116,179,16,1,104,2,254,167,86,255,55,122,244'
print(solve(list(range(256)), [int(n) for n in data.split(',')]))


assert solve2(to_lengths('')) == 'a2582a3a0e66e6e86e3812dcb672a272'
assert solve2(to_lengths('AoC 2017')) == '33efeb34ea91902bb2f59c9920caa6cd'
assert solve2(to_lengths('1,2,3')) == '3efbe78a8d82f29979031a4aa0b16a9d'
assert solve2(to_lengths('1,2,4')) == '63960835bcdc130f0b66d7ff4f6a5a8e'
print(solve2(to_lengths(data)))
