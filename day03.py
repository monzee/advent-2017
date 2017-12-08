import math
import itertools


def solve(n):
    if n == 1:
        return 0
    r = math.ceil(math.sqrt(n)) // 2
    base = (r - 1)**2
    return r + (n - base) % r


assert solve(1) == 0
assert solve(12) == 3
assert solve(23) == 2
assert solve(1024) == 31
print(solve(277678))


def solve2(floor, grid={(0, 0): 1}):
    for p in spiral_path():
        value = grid.get(p, None) or sum(grid.get(q, 0) for q in neighbors(*p))
        grid[p] = value
        if value > floor:
            return value


def spiral_path(radius=1):
    while True:
        length = radius*2 + 1
        pattern = [radius]*length + list(range(radius - 1, -radius, -1))
        pattern += [-n for n in pattern]
        xs = pattern[1:] + [radius]
        ys = pattern[length:] + pattern[:length]
        yield from zip(xs, ys)
        radius += 1


def neighbors(x, y):
    return (((x + dx), (y + dy)) for (dx, dy) in RING_1)


RING_1 = list(itertools.islice(spiral_path(), 8))

assert solve2(100) == 122
assert solve2(200) == 304
assert solve2(500) == 747
print(solve2(277678))


'''
1

5 4 3
6   2
7 8 9

17 16 15 14 13
18          12
19          11
20          10
21 22 23 24 25

37 36 35 34 33 32 31
38                30
39                29
40                28
41                27
42                26
43 44 45 46 47 48 49



ring 1 = 2..9 =   1**2+1 .. 3**2
ring 2 = 10..25 = 3**2+1 .. 5**2
ring 3 = 26..49 = 5**2+1 .. 7**2


ring r = let d = r * 2 in (d-1)**2+1..(d+1)**2


radius n = (ceil (sqrt n)) // 2
radius 60 = 8 // 2 = 4
radius 123 = 12 // 2 = 6

check:
ring 4 = 50..81
ring 5 = 82..121
ring 6 = 122..169


axes 1 = [2, 4, 6, 8]
axes 2 = [11, 15, 19, 23]
axes 3 = [28, 34, 40, 46]

axes r = let d = r*2, a0 = (d-1)**2 + r in [a0, a0 + d, a0 + 2*d, a0 + 3*d]



m[0, 0] = 1

m[ 1,  0] = 1
m[ 1,  1] = 2
m[ 0,  1] = 4
m[-1,  1] = 5
m[-1,  0] = 10
m[-1, -1] = 11
m[ 0, -1] = 23
m[ 1, -1] = 25

1 1 1 0 -1 -1 -1 0

m[ 2, -1] = 26
m[ 2,  0] = 54
m[ 2,  1] = 57
m[ 2,  2] = 59
m[ 1,  2] = 122
m[ 0,  2] = 133
m[-1,  2] = 142
m[-2,  2] = 147
m[-2,  1] = 304
m[-2,  0] = 330
m[-2, -1] = 351
m[-2, -2] = 362
m[-1, -2] = 747
m[ 0, -2] = 806
m[ 1, -2] = ...
m[ 2, -2] = ...

2 2 2 2 2 1 0 -1 -2 -2 -2 -2 -2 -1 0 1

3 3 3 3 3 3 3 2 1 0 -1 -2 -3 -3 -3 -3 -3 -3 -3 -2 -1 0 1 2
'''
