from typing import Iterable, List, Optional, Dict, Set, Tuple
import re


class Node:
    name: str
    weight: int
    children: List['Node']
    _total: Optional[int] = None

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.children = []

    @property
    def total_weight(self) -> int:
        if not self._total:
            self._total = self.weight + sum(c.total_weight
                                            for c in self.children)
        return self._total

    def balance(self, target_weight: int=0) -> Optional[Tuple['Node', int]]:
        distinct = find_different(self.children)
        if distinct:
            return distinct.balance(next(c.total_weight
                                         for c in self.children
                                         if c != distinct))
        elif target_weight:
            return self, self.total_weight - target_weight
        else:
            return None


def find_different(xs: List[Node]) -> Optional[Node]:
    if len(xs) < 3:
        return None
    a, b, c, *rest = xs
    va, vb, vc = [e.total_weight for e in [a, b, c]]
    if va == vb == vc:
        if not rest:
            return None
        else:
            return find_different(rest + xs[:3 - len(rest)])
    elif vb == vc:
        return a
    elif va == vc:
        return b
    else:
        return c


def parse(lines: Iterable[str]) -> Node:
    pattern = re.compile(r'(\w+) \((\d+)\)(?: -> ([\w, ]+))?')
    nodes: Dict[str, Node] = {}
    edges: Dict[str, List[str]] = {}
    roots: Set[str] = set()
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
        name = match.group(1)
        roots.add(name)
        nodes[name] = Node(name, int(match.group(2)))
        children = match.group(3)
        if children:
            edges[name] = children.split(', ')
    for name, children_names in edges.items():
        children = nodes[name].children
        for child in children_names:
            roots.discard(child)
            children.append(nodes[child])
    assert len(roots) == 1, 'graph is not a tree'
    return nodes[roots.pop()]


test_data = '''
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
'''
test = parse(test_data.splitlines())
bad, delta = test.balance()
assert test.name == 'tknk'
assert bad.weight - delta == 60
with open('input07') as f:
    root = parse(f.readlines())
    answer, delta = root.balance()
    print(root.name, answer.name, answer.weight - delta)
