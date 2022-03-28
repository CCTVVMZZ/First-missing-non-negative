from typing import Any
from collections.abc import Callable, MutableSequence
from numbers import Integral


def is_in_range(start: Integral, stop: Integral | None = None, step: Integral = 1):
    """
    A naive implementation would be:
    return lambda x: x in range(start, stop, step)

    >>> all(is_in_range(stop)(x) for x, stop in [(5, 8), (0, 5), (3, 4)])
    True
    >>> any(is_in_range(stop)(x) for x, stop in [(8, 5), (-1, 3), (4, 4), (-10, 0), (-2, - 1)])
    False
    >>> all(is_in_range(start, stop)(x) for x, start, stop in [(3, 2, 8), (3, 3, 4), (1, -1, 2)])
    True
    >>> any(is_in_range(start, stop)(x) for x, start, stop in [(0, 2, 8), (4, -3, 4), (8, 2, 5)])
    False
    >>> all(is_in_range(start, stop, step)(x) for x, start, stop, step in [(9, 1, 15, 4), (0, 8, -3, -2)])
    True
    >>> any(is_in_range(start, stop, step)(x) for x, start, stop, step in [(2, 1, 9, 2), (7, 2, 7, 2), (-6, 1, -10, - 3)])
    False
    """
    
    def wrapped(x):
        if not isinstance(x, Integral):
            return False
        q, r = divmod(x - start, step)
        if r != 0 or q < 0:
            return False
        if step > 0:
            return x < stop
        return x > stop
        
    if step == 0: raise ValueError("is_in_range() arg 3 must not be zero")
    if stop is None:
         start, stop = 0, start
    return wrapped


def segregate(T: MutableSequence, p: Callable) -> int:
    """
    >>> p = lambda x: bool(x)
    >>> T = []; segregate(T, p); T
    0
    []
    >>> T = [0]; segregate(T, p); T
    0
    [0]
    >>> T = [1]; segregate(T, p); T
    1
    [1]
    >>> T = [1, 1]; segregate(T, p); T
    2
    [1, 1]
    >>> T = [0, 0, 0]; segregate(T, p); T
    0
    [0, 0, 0]
    >>> T = [0, 1, 1, 0]; segregate(T, p); T
    2
    [1, 1, 0, 0]
    >>> T = [1, 0, 1, 0, 1]; segregate(T, p); T
    3
    [1, 1, 1, 0, 0]
    >>> T = [1, 1, 1, 0, 0, 0]; segregate(T, p); T
    3
    [1, 1, 1, 0, 0, 0]

    If T != [] then the predicate p is called exactly len(T) times.
   """
    if not T:
        return 0
    i = 0
    j = len(T) - 1
    while i < j:
        # invariant: all(p(t) for t in T[:i])
        # invariant: not any(p(t) for t in T[j + 1:])
        if p(T[i]):
            i += 1
        else:
            T[i], T[j] = T[j], T[i]
            j -= 1
    return i + bool(p(T[i]))

def FMNN_naive(T: MutableSequence) -> int:
    """
    The time complexity is quadratic in len(T).
    The space complexity is bounded.
    """    
    n = 0
    while n in T:
        n += 1
    return n

def FMNN_sort(T: MutableSequence) -> int:
    """
    The time complexity is linearithmic in len(T).
    The space complexity is that of timsort;
    it could be bounded if timsort was replaced with, say, heapsort.
    """
    
    n = len(T)
    T.sort(key = lambda x: x if is_in_range(n)(x) else n)
    n = 0
    it = iter(T)
    while n in it: n += 1
    return n


def FMNN_linear_linear(T: MutableSequence) -> int:
    """
    The time complexity is linear in len(T).
    The space complexity is also linear in len(T).
    """
    
    is_here = [False] * (len(T) + 1)
    for t in T:
        if is_in_range(len(T))(t):
            is_here[t] = True
    n = 0
    while is_here[n]:
        n += 1
    return n
    
T = [7, 5, 8, 0, 3, "toto", 1, 15, 2, 5, 2, 0, 1, 5, "aze"]
print(FMNN_sort(T))
        
if __name__ == "__main__":
    print("Entering doctest mode !")
    import doctest
    doctest.testmod()   
