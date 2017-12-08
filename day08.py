from typing import NamedTuple, Callable, Iterable, Dict, Tuple
import re
import collections
import operator as op
import functools as ft


class Instruction(NamedTuple):
    key: str
    cmd: Callable[[int], int]
    cmp_key: str
    pred: Callable[[int], bool]


def parse(lines: Iterable[str]) -> Iterable[Instruction]:
    pattern = re.compile(r'''
    (\w+)\ (inc|dec)\ (-?\d+)\ if\ (\w+)\ (<|>|==|!=|<=|>=)\ (-?\d+)
    ''', re.X)
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
        by = int(match.group(3))
        if match.group(2) == 'inc':
            cmd = ft.partial(op.add, by)
        else:
            cmd = ft.partial(op.add, -by)
        left = match.group(4)
        comparator = match.group(5)
        right = int(match.group(6))
        if comparator == '<':
            pred = ft.partial(op.gt, right)
        elif comparator == '>':
            pred = ft.partial(op.lt, right)
        elif comparator == '==':
            pred = ft.partial(op.eq, right)
        elif comparator == '!=':
            pred = ft.partial(op.ne, right)
        elif comparator == '<=':
            pred = ft.partial(op.ge, right)
        elif comparator == '>=':
            pred = ft.partial(op.le, right)
        yield Instruction(match.group(1), cmd, left, pred)


def exec(program: Iterable[Instruction]) -> Dict[str, int]:
    registers: Dict[str, int] = collections.defaultdict(int)
    for instr in program:
        if instr.pred(registers[instr.cmp_key]):
            result = instr.cmd(registers[instr.key])
            registers[instr.key] = result
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
