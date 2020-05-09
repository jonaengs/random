from abc import ABC
from copy import deepcopy
from collections.abc import Iterable

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

    def groupby(self, id_func):
        groups = dict()
        groups.setdefault(list())
        for elem in self:
            groups[id_func(elem)] += list([elem])
        return groups

    def exists(self):
        return bool(self)

    def isempty(self):
        return not bool(self)

    @property
    def length(self):
        return self.__len__()


class list(list, IterableMethods):

    def __init__(self, seq=(), *args):
        """ Allow list(1, 2, 3) etc. 
        []-constructor creates standard python list"""
        if args or not hasattr(seq, '__iter__'):
            seq = (seq, *args)
        return super().__init__(seq)

    def flatten(self, all_iterables=False):
        flattened = list()
        for elem in self:
            if type(elem) == self.__class__ \
                or (all_iterables and isinstance(elem, Iterable)):
                flattened += elem.flatten()
            else:
                flattened.append(elem)
        return self.__class__(flattened)

    def __iadd__(self, other):
        return self + other


class tuple(tuple, IterableMethods):
    """ Allow tuple(1, 2, 3) etc. 
    (,)-constructor creates standard python tuple"""
    def __new__(cls, seq=(), *args):
        if args or not hasattr(seq, '__iter__'):
            seq = (seq, *args)
        return super().__new__(cls, seq)


class dict(dict):
    def __getitem__(self, key):
        try:
            item = super().__getitem__(key)
        except KeyError as key_error:
            try:
                item = self.default_value
            except AttributeError:
                raise key_error from None
        return item
    
    def setdefault(self, default_value):
        self.default_value = default_value

    def getdefault(self):  # let fail
        return self.default_value

    def hasdefault(self):
        try:
            self.default_value
        except AttributeError:
            return False
        return True


def partial(func, *args, **kwargs):
    def temp(*extra_args, **extra_kwargs):
        return func(*args, *extra_args, **kwargs, **extra_kwargs)
    return temp


def poly(*coefficients, x):
    return sum(constant * x**i for i, constant in enumerate(reversed(coefficients)))


p_a1_b4_c4 = partial(poly, 1, 4, 4)
assert p_a1_b4_c4(x=-2) == 0

product = partial(list(1,2,3).reduce, lambda acc, x: acc * x)
assert product(0) == 0 and product(1) == 6
