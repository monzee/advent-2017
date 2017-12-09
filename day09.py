from typing import Tuple


def solve(chars: str) -> Tuple[int, int]:
    depth = 0
    score = 0
    garbage = 0
    state = 'root'
    for c in chars.strip():
        if state == 'root':
            if c == '{':
                depth += 1
                state = 'group'
            else:
                raise ValueError('at state {}, unexpected {}'.format(state, c))
        elif state == 'group':
            if c == '{':
                depth += 1
            elif c == '<':
                state = 'garbage'
            elif c == '}':
                score += depth
                depth -= 1
                if depth == 0:
                    state = 'root'
            elif c == ',':
                pass
            else:
                raise ValueError('at state {}, unexpected {}'.format(state, c))
        elif state == 'garbage':
            if c == '!':
                state = 'escape'
            elif c == '>':
                state = 'group'
            else:
                garbage += 1
        elif state == 'escape':
            state = 'garbage'
    return score, garbage


assert solve('{}')[0] == 1
assert solve('{{{}}}')[0] == 6
assert solve('{{},{}}')[0] == 5
assert solve('{<>}')[1] == 0
assert solve('{<random characters>}')[1] == 17
assert solve('{<<<<>}')[1] == 3
assert solve('{<{!>}>}')[1] == 2
assert solve('{<!!>}')[1] == 0
assert solve('{<!!!>>}')[1] == 0
assert solve('{<{o"i!a,<{i<a>}')[1] == 10

with open('input09') as f:
    print(solve(f.read()))
