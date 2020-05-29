from collections import Counter
from itertools import combinations
from functools import reduce

transactions = (
    "BF",
    "ABCDFH",
    "ABF",
    "ABFH",
    "ADEF",
    "ABFH",
    "ABDEFH",
    "AGH",
)
transactions = tuple(sorted(transactions)) # NOTE: sort transactions alphabetically.
min_count = 4


def get_frequent_sets(i, min_count=min_count):
    all_sets= reduce(lambda x, y: x + y, (Counter("".join(c) for c in combinations(t, i)) \
        for t in transactions))
    frequent_sets = dict(filter(lambda kv: kv[1] >= min_count, all_sets.items()))
    return frequent_sets


def order_transactions(min_count=min_count):  # call with 0 to include all chars in ordering
    freqs = get_frequent_sets(1, min_count=0)
    ts = (filter(lambda c: freqs[c] >= min_count, t) for t in transactions)
    order = lambda c: freqs[c]
    return tuple("".join(sorted(list(t), reverse=True, key=order)) for t in ts)


def print_all_frequencies(min_count=min_count):
    print("\nFrequencies:")
    for i in range(1, max(len(t) for t in transactions) + 1):
        print(f"{i}:\t{get_frequent_sets(i, min_count)}")


def print_ordered_transactions(min_count=min_count):
    print("\nOrdered Transactions:", end="\n\t")
    for t in order_transactions(min_count=min_count):
        print(t, end="\n\t")
    print()


print_all_frequencies()
print_ordered_transactions()