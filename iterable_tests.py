# "tests" in the loosest meaning
from iterable_methods import list, tuple, dict
from copy import deepcopy

def dict_tests():
    d = dict(a=1, b=2)
    assert d['a'] == 1
    assert not d.hasdefault()
    
    try:
        d['c']
    except KeyError:
        pass
    else:
        raise Error("KeyError should have been raised")

    d.setdefault(0)
    assert d.hasdefault
    assert d['c'] == 0


def itermethods_test():
    for _cls in (list, tuple):
        assert not isinstance([], _cls)
        assert all(
            isinstance(elem, _cls) for elem in 
            (_cls(), _cls(1), _cls(1,2,3), _cls(_cls()), _cls(_cls(), _cls()), _cls(range(10)), _cls(i for i in range(10)))
        )

        a = _cls(10, 1, 2, 3)
        a_copy = deepcopy(a)
        assert a.foldl(lambda x, y: x - y, base=0) == -16
        assert a.foldr(lambda x, y: x - y, base=0) == 8  # 10 - (1 - (2 - (3 - 0))) = 10 - (1 - (-1))
        assert a == a_copy  # fold never changes the original object

        items = _cls(_cls(i, i*2, i**2, i//2, i%6) for i in range(0, 37, 3))
        assert items\
            .filter(lambda l: any("5" in str(i) for i in l))\
                .map(lambda l: l[0])\
                    .exclude(lambda n: n % 2 == 0)\
                        .length == 2

        fruits = _cls("apple", "pear", "banana", "pineapple")
        assert fruits.groupby(lambda f: f[0]) == dict({'a': ['apple'], 'p': ['pear', 'pineapple'], 'b': ['banana']})


def list_tests():
    nested = list(list(list(1, 2), 3, 4, list(5, 6)), 7)
    assert nested.flatten() == list(range(1, 8))

    a = list(1, 2, 3)
    b = a
    a += list(4, 5)
    assert b != a, "+= operation should no longer mutate"





itermethods_test()
dict_tests()
list_tests()