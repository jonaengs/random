from abc import ABC

class IterableMethods(ABC):  # abstract class

    def __str__(self):
        return "c" + super().__str__()

    def map(self, func):
        return self.__class__(map(func, self))

    def foreach(self, func):
        for elem in self:
            func(elem)

    def filter(self, pred):
        return self.__class__(filter(pred, self))

    def exclude(self, pred):
        return self.__class__(self.filter(lambda x: not pred(x)))

    def reduce(self, func, base=None, reverse=False):
        if self.isempty():
            return base
        iterator = self.__iter__() if not reverse else reversed(self)
        acc = base if base is not None else next(iterator) 
        for elem in iterator:
            acc = func(acc, elem)
        return acc

    def foldl(self, func, base):
        return self.reduce(func, base)

    def foldr(self, func, base):
        reverse_func = lambda acc, x: func(x, acc)
        return self.reduce(reverse_func, base, reverse=True)

    def exists(self):
        return bool(self)

    def isempty(self):
        return not bool(self)

    @property
    def length(self):
        return self.__len__()


class list(list, IterableMethods):

    def __init__(self, seq=(), *args):
        """ Allow list(1, 2, 3) etc. Note behavior when passing one vs multiple iterables: 
            list([]) = []
            list([], []) = [[], []] """
        if args or not hasattr(seq, '__iter__'):
            seq = (seq, *args)
        return super().__init__(seq)


class tuple(tuple, IterableMethods):

    def __new__(cls, seq=(), *args):
        if args or not hasattr(seq, '__iter__'):
            seq = (seq, *args)
        return super().__new__(cls, seq)



# Sanity checks (aka crappy tests)
for _cls in (list, tuple):
    assert not isinstance([], _cls)
    assert all(
        isinstance(elem, _cls) for elem in 
        (_cls(), _cls(1), _cls(1,2,3), _cls(_cls()), _cls(_cls(), _cls()), _cls(range(10)), _cls(i for i in range(10)))
    )

    a = _cls(10, 1, 2, 3)
    assert a.foldl(lambda x, y: x - y, base=0) == -16
    assert a.foldr(lambda x, y: x - y, base=0) == 8  # 10 - (1 - (2 - (3 - 0))) = 10 - (1 - (-1))

    items = _cls(_cls(i, i*2, i**2, i//2, i%6) for i in range(0, 37, 3))
    assert items\
        .filter(lambda l: any("5" in str(i) for i in l))\
            .map(lambda l: l[0])\
                .exclude(lambda n: n % 2 == 0)\
                    .length == 2


def partial(func, *args, **kwargs):
    def temp(*extra_args, **extra_kwargs):
        return func(*args, *extra_args, **kwargs, **extra_kwargs)
    return temp

def poly(*coefficients, x):
    return sum(constant * pow(x, i) for i, constant in enumerate(reversed(coefficients)))


p_a1_b4_c4 = partial(poly, 1, 4, 4)
assert p_a1_b4_c4(x=-2) == 0

product = partial(list(1,2,3).reduce, lambda acc, x: acc * x)
assert product(0) == 0 and product(1) == 6

