from inspect import signature

class list(list):
    def __init__(self, seq=(), *args):
        """
        Since [1, 2, 3] return base list, allow list(1, 2, 3) etc. 
        Note behavior when passing one vs multiple iterators: 
            list([]) = []
            list([], []) = [[], []]
        """
        if args or not hasattr(seq, '__iter__'):
            seq = (seq, *args)
        return super(list, self).__init__(seq)

    def __str__(self):
        return "c" + super(list, self).__str__()

    def map(self, func):
        return list(map(func, self))

    def foreach(self, func):
        for elem in self:
            func(elem)

    def filter(self, pred):
        return list(filter(pred, self))

    def exclude(self, pred):
        return list(self.filter(lambda x: not pred(x)))

    def reduce(self, func, base=None):
        if self.isempty(): 
            return base
        iterator = self.__iter__()
        acc = next(iterator) if base is None else base
        for elem in iterator:
            acc = func(acc, elem)
        return acc

    def foldl(self, func, base):
        return self.reduce(func, base)

    def foldr(self, func, base):
        reverse_func = lambda acc, x: func(x, acc)
        return list.reduce(reversed(self), reverse_func, base)

    def exists(self):
        return bool(self)

    def isempty(self):
        return not bool(self)


def partial(func, *args, **kwargs):
    def temp(*remaining_args, **remaining_kwargs):
        return func(*args, *remaining_args, **kwargs, **remaining_kwargs)
    return temp

def f(*args, **kwargs):
    return args + tuple(kwargs.items())

p1 = partial(f, 1, 2, 3, 4, a=1)
p2 = partial(p1, 5, 6, 7, b=2)
print(p2(100))

product = partial(list(1,2,3).reduce, lambda acc, x: acc * x)
print(product(0), product(1))


a = list(10, 1, 2, 3)
# print(a.foldl(lambda x, y: x - y, base=0))
# print(a.foldr(lambda x, y: x - y, base=0))

assert not isinstance([], list)
assert all(
    isinstance(elem, list) for elem in 
    (a, list(), list(1), list(1,2,3), list([]), list([], []), list([1,2], [1]))
)
