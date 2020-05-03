class ListOperations(type):
    def __call__(cls, *args):
        if cls == List:
            if not args:
                return Nil
            return type.__call__(Cons, args[0], List(*args[1:]))
        elif cls == Cons:
            return type.__call__(Cons, args[0], args[1])

    def __add__(self, appendage):  # concat 
        assert self.isempty
        return appendage

    def __rshift__(cls, head):  # prepend
        assert self.isempty
        return Cons(head, cls)

    def __lshift__(cls, head):
        raise ValueError("Cannot append to nil")


class List(metaclass=ListOperations):
    def __rshift__(self, head):
        return Cons(head, self)

    def __lshift__(self, tail):
        return self + List(tail)

    @property
    def isempty(self):
        raise ValueError("not implemented")


class Cons(List):
    isempty = False

    def __init__(self, head, tail):
        self._head = head
        self._tail = tail

    def __add__(self, appendage):  # concat   
        return Cons(self.head, self.tail + appendage)

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail


class Nil(List):
    isempty = True

    def __new__(cls, *args, **kwargs):
        raise ValueError("Nil is not meant to be instantiated")

    @classmethod
    @property
    def head(cls):
        raise ValueError("Nil.head")

    @classmethod
    @property
    def tail(cls):
        raise ValueError("Nil.tail")


l = List(*range(1, 10))
l = l + List(*range(10, 20))
l = l >> 0
l = l << 20
while not l.isempty:
    print(l.head)
    l = l.tail
