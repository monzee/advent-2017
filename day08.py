from typing import NamedTuple, Callable, Iterable, Dict, Tuple
import re
import collections
import operator
from functools import partial


class Instruction(NamedTuple):
    register: str
    cmd: Callable[[int], int]
    pred: Tuple[str, Callable[[int], bool]]


def parse(lines: Iterable[str]) -> Iterable[Instruction]:
    pattern = re.compile(r'''
    (\w+)\ (inc|dec)\ (-?\d+)\ if\ (\w+)\ (<|>|==|!=|<=|>=)\ (-?\d+)
    ''', re.X)
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
        cmd = match.group(2)
        by = int(match.group(3))
        if cmd == 'inc':
            cmd = partial(operator.add, by)
        else:
            cmd = partial(operator.add, -by)
        left = match.group(4)
        cmp = match.group(5)
        right = int(match.group(6))
        if cmp == '<':
            pred = (left, partial(operator.gt, right))
        elif cmp == '>':
            pred = (left, partial(operator.lt, right))
        elif cmp == '==':
            pred = (left, partial(operator.eq, right))
        elif cmp == '!=':
            pred = (left, partial(operator.ne, right))
        elif cmp == '<=':
            pred = (left, partial(operator.ge, right))
        elif cmp == '>=':
            pred = (left, partial(operator.le, right))
        yield Instruction(match.group(1), cmd, pred)


def exec(program: Iterable[Instruction]) -> Dict[str, int]:
    registers: Dict[str, int] = collections.defaultdict(int)
    for instr in program:
        left, pred = instr.pred
        if pred(registers[left]):
            e = registers[instr.register]
            result = instr.cmd(e)
            registers[instr.register] = result
            registers[''] = max(result, registers[''])
    return registers


def solve(registers: Dict[str, int]) -> Tuple[int, int]:
    return max(v for k, v in registers.items() if k), registers['']


test_program = '''
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
'''
assert solve(exec(parse(test_program.splitlines()))) == (1, 10)
with open('input08') as f:
    print(solve(exec(parse(f.readlines()))))
