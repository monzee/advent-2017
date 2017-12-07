def solve(jumps, alt=False):
    goal = len(jumps)
    at = 0
    count = 0
    while 0 <= at < goal:
        j = jumps[at]
        if alt and j >= 3:
            jumps[at] -= 1
        else:
            jumps[at] += 1

        at += j
        count += 1
    return count


assert solve([0, 3, 0, 1, -3]) == 5
assert solve([0, 3, 0, 1, -3], True) == 10
with open('input05') as f:
    print(solve([int(line.strip()) for line in f.readlines() if line], True))
