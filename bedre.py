"""
Lessons:
1. Know comprehensions and anonymous (lambda) functions
2. Know the built-in functions
    And pay attention to their optional arguments
3. Know the data types
    Know what is mutable and what as not, and what that entails
    Know when to use lists, tuples, dicts
    Know the difference between iterable, indexable
    Know what about generators
4. Know the stdlib. Especially: itertools, collections
    also useful: random, functools, 
5. Know about libraries and modules
    * numpy
    * PIL
    * scipy
    * pytorch, keras, pyro, scikit, tensforflow
    * django, flask, fastAPI
    * matplotlib and seaborn

    * ipython
6. Know the "with" keyword


(7. Know how *args, **kwargs, multi-variable assignment work)
(8. Nested functions, default arguments and closures)
(9. For-else)
(10. Know when to use classes and when to just put stuff in a file)
(11. Know about decorators)
"""

# Filling out a list:
# standard way
l = []
for i in range(10):
    l.append(i)

# better (using list comprehensions)
l = [i for i in range(10)]

# even better
l = list(range(10))


# Indexing items from a list
l = list(range(10))
idxs = [0, 2, 5, 7]

# standard way
result = []
for idx in idxs:
    result.append(l[idx])

# better (using list comprehensions)
result = [l[idx] for idx in idxs]

# even better (if you are using numpy)
import numpy as np
result = np.array(l)[idxs]


# Filling out a dictionary
# standard way
keys = list(range(10))
vals = [chr(i + ord("A")) for i in keys]
result = {}
for i in range(len(keys)):
    result[keys[i]] = vals[i]

# using comprehensions 1
keys = list(range(10))
vals = [chr(i + ord("A")) for i in keys]
result = {keys[i]: vals[i] for i in range(len(keys))}

# using zip
keys = list(range(10))
vals = [chr(i + ord("A")) for i in keys]
result = dict(zip(keys, vals)) # dict(((0, "A"), (1, "B"))) => {0: "A", 1: "B"}

# using comprehensions 2
result = {i: chr(ord("A") + i) for i in range(10)}

# if you only have values, use enumerate:
vals = ["A", "B", "C", "D"]
result = dict(enumerate(vals))


# Combining dictionaries:
d1, d2 = {1: 2}, {3: 4}
d = {**d1, **d2}
# d = d1 | d2  # only works in 3.9 or higher



# Know the built-in functions:

# Sum
# standard
items = [1, 5, 7, 10, 12]
total = 0
for item in items:
    total += item

# better
total = sum(items)


# All & Any
bools = [True, True, False, True]
# standard
any_true = False
all_true = True
for b in bools:
    if b:  # obvious: dont do "if b == True"
        any_true = True
    else:
        all_true = False

# slightly better
for b in bools:
    any_true |= b  # any_true = any_true or b
    all_true &= b  # all_true = all_true and b

# another approach
any_true = sum(bools) > 0
all_true = sum(bools) == len(bools)  # from math import prod; all_true = prod(bools) == 1

# better
any_true, all_true = any(bools), all(bools)  # even better: they stop early


# Map and Filter
elems = list(range(10))
# using comprehensions
squared = [e**2 for e in elems]
evens = [e for e in elems if e % 2 == 0]
# using map & filter
squared = map(lambda x: x**2, elems)
evens = filter(lambda x: x % 2 == 1, elems)  # "x == 1" is slightly redundant for mod 2, as in python True=1 and False=0. But being explicit about it is nice
# doesn't seem any nicer? Can be great for readibility if the functions are predefined:
def square(x): return x * x
def is_odd(x): return x % 2 == 1
squared = map(square, elems)
evens = filter(is_odd, elems)
# can use these with any, all and sum
contains_odd = any(map(is_odd, elems))
num_odd = sum(map(is_odd, elems))  # since True=1 and False=0, we can sum over them
num_odd = len(list(filter(is_odd, elems)))
sum_of_odds = sum(filter(is_odd, elems))

# Min, Max and Sorting
vals = [5, 1, 3, 0, 7, -3]
min_val, max_val = min(vals), max(vals)
sorted_vals = sorted(vals)

# how about sorting slightly more complex data structures?
vals = [(5, "C"), (-1, "B"), (10, "D"), (3, "A")]
sorted_by_num = sorted(vals)
# how would you sort this by the second item (characters) though
chars = sorted([t[1] for t in vals])
sorted_by_char = [
    ([v[0] for v in vals if v[1] == char][0], char)
    for char in chars
]
# or 
map(tuple, map(reversed, sorted(map(tuple, map(reversed, vals)))))
# or
def reverse_tuple(t): return tuple(reversed(t))
map(reverse_tuple, sorted(map(reverse_tuple, vals)))
# or
[(t[1], t[0]) for t in sorted((t[1], t[0]) for t in vals)]

# use "key" argument to specify attribute
def get_char(t):
    return t[1]
min_char, max_char = min(vals, key=get_char), max(vals, key=get_char)
# use "reverse" flag to get descending 
sorted_by_char_desc = sorted(vals, key=get_char, reverse=True)
# later: use itemgetter from operators lib and set key=itemgetter(1)


# Stdlib functions and classes

# Random library: random.choice(s), random.sample
import random
# use random.range instead of random.randint. randint is inclusive of the end range. randrange is not (like python range)
n = 5
randints = [random.randint(0, n) for _ in range(100)]
randranges = [random.randrange(n) for _ in range(100)]
all(r in range(n) for r in randints)  # False
all(r in range(n) for r in randranges)  # True
# use random.choice to get a random item from a list, use random.choices to get multiple. 
random.choice(range(n))
random.choices(range(n), k=3)
random.choices(range(n), k=3, weights=range(n)) # can specify weights (relative or cumulative) for each

# The collections library is fantastic!
alphabet = "".join(map(chr, range(ord("A"), ord("Z") + 1)))
vals = random.choices(alphabet, k=100)
# Defaultdict
from collections import defaultdict
count = defaultdict(int)
for c in vals:
    count[c] += 1
# Counter: counts occurences in an iterable
from collections import Counter
count = Counter(vals)
top3 = count.most_common(3)
# Namedtuple: tuples with named members
from collections import namedtuple
Color = namedtuple("Color", ("r", "g", "b"))
red = Color(255, 0, 0)
yellow = Color(255, 255, 0)
grey = Color(r=122, g=122, b=122)
mix = Color(red.r, yellow.g, grey.b)

# Functools: partial
from functools import partial
def f(x, y):
    return x * y
double = partial(f, 2)
triple = partial(f, 3)
double(2) == 4
triple(2) == 6

# Itertools: product, combinations, permutations, chain, cycle, groupby
from itertools import product, combinations
vals = range(0, 256, 8)
many_colors = product(vals, vals, vals)
some_colors = combinations(vals, 3)
from itertools import cycle
nums = [random.randrange(10000) for _ in range(100)]
mask = [511, 634, 785, 9999]
masked_ = [n ^ m for n, m in zip(nums, cycle(mask))]

from PIL import Image
import numpy as np
from math import sqrt
image_data = np.array(list(many_colors), dtype=np.uint8)
sqrt_size = int(sqrt(image_data.size / 3))
image_data.resize(sqrt_size**2, 3)
image_data = image_data.reshape(sqrt_size, sqrt_size, 3)
im = Image.fromarray(image_data, mode="RGB")
# im.show()

# Operator: itemgetter
from operator import itemgetter
from itertools import chain, groupby
vals = [(1, 2), (2, 1), (3, -1), (-1, 5)]
list(sorted(vals, key=itemgetter(1)))
vals = [{1: "a"}, {1: "b"}, {1: "a", 2: "c"}]
list(sorted(vals, key=itemgetter(1)))
vals = dict(list(chain(*list(chain(tuple(reversed(d.items())) for d in vals)))))
vals = [{1: "a"}, {1: "b"}, {1: "a", 2: "c"}]
vals = dict((k, list(g)) for k, g in groupby(vals, key=lambda d: d.values()))
print(vals)

# Dataclasses: dataclass - like a namedtuple but with mutability and typing
from dataclasses import dataclass
from typing import Optional
@dataclass
class LinkedList:
    content: int
    next: Optional['LinkedList'] = None

ll = LinkedList(1, LinkedList(2, LinkedList(3)))
ll.next.content = -1

# Noen enkle kodeoppgaver:

# hent ut alle verdier fra treet (chars som danner en streng)
class Tree:
    ...

class Branch(Tree):
    def __init__(self, left_child, right_child):
        self.left = left_child
        self.right = right_child

class Leaf(Tree):
    def __init__(self, content):
        self.content = content

tree = Branch(
    Branch(
        Leaf("c"),
        Branch(
            Branch(
                Leaf("d"),
                Leaf("e")
            ),
            Leaf("f")
        )
    ),
    Branch(
        Leaf("a"),
        Leaf("b")
    )
)

# standard? Iterativ depth first search
def extract_values(tree):
    result = ""
    branches = [tree]
    while branches:
        branch = branches.pop(0)
        if type(branch) == Leaf:
            result += branch.content
        else:
            branches += [branch.left, branch.right]
            
    return result

print(extract_values(tree))

# rekursiv depth first search
def extract_values(tree):
    result = ""
    if type(tree) == Leaf:
        result += tree.content
    else:
        for branch in (tree.left, tree.right):  # or: result += ext_vals(left) + ext_vals(right)
            result += extract_values(branch)
    
    return result

print(extract_values(tree))

# kortet litt ned 
def extract_values(tree):
    if type(tree) == Leaf:
        return tree.content
    
    return extract_values(tree.left) + extract_values(tree.right)

print(extract_values(tree))

# enda kortere (men ikke like lesbart?)
def extract_values(tree):
    return getattr(tree, "content", None) or "".join(map(extract_values, (tree.left, tree.right)))
    
    return tree.content if type(tree) == Leaf else "".join(map(extract_values, (tree.left, tree.right)))
    
    return getattr(tree, "content", None) or extract_values(tree.left) + extract_values(tree.right)

print(extract_values(tree))

