import re
import itertools


def solve(words):
    return len([phrase for phrase in words if valid(phrase)])


def valid(passphrase):
    words = re.split(r'\s+', passphrase.strip())
    return passphrase and \
        len(words) == len(set(words)) and \
        not any(are_anagrams(*p) for p in itertools.combinations(words, 2))


def are_anagrams(a, b):
    return ''.join(sorted(a)) == ''.join(sorted((b)))


assert valid('aa bb cc dd ee')
assert not valid('aa bb cc dd aa')
assert valid('aa bb cc dd aaa')
assert are_anagrams('a', 'a')
assert not are_anagrams('a', 'aa')
assert are_anagrams('ab', 'ba')
assert valid('abcde fghij')
assert not valid('abcde xyz ecdab')
assert valid('a ab abc abd abf abj')
assert valid('iiii oiii ooii oooi oooo')
assert not valid('oiii ioii iioi iiio')

with open('input04') as f:
    print(solve([line.strip() for line in f.readlines()]))
