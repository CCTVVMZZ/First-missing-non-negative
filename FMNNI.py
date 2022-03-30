"""
The First Missing Non-Negative Integer (FMNNI) problem is defined as follows:
 
given a container T, find the smallest non-negative integer that is not in T.

This module supplies 4 distinct functions that solve the FMNNI problem on lists: 
FMNNI_naive, 
FMNNI_sort, 
FMNNI_linear_linear, and 
FMNNI_linear_const.

>>> test = lambda T: (FMNNI_naive(T), FMNNI_sort(T.copy()), FMNNI_linear_linear(T), FMNNI_linear_const(T.copy())) 
>>> T = []; test(T)
(0, 0, 0, 0)
>>> T = [0]; test(T)
(1, 1, 1, 1)
>>> T = [0, 1, 2, 3]; test(T) 
(4, 4, 4, 4)
>>> T = [1, 3, 2, 0]; test(T)  
(4, 4, 4, 4)
>>> T = [4, 1, 0, 5]; test(T)  
(2, 2, 2, 2)
>>> T = list("123456789"); test(T) 
(0, 0, 0, 0)
>>> T = [0, 101, 1, 103, 0, 100, 101, 100, 2, 4, 0, 2, 1, 1, 103, 2, 0, 1]; test(T)
(3, 3, 3, 3)
>>> import numpy as np
>>> T = [np.int8(t) for t in T]; test(T)  
(3, 3, 3, 3)
>>> T = [7, 5, np.uint32(8), 0, np.int64(3), "toto", 1, 150000, 2, 3.14159, 5, -6, 2, 0, 1, 5, "caca"]; test(T)
(4, 4, 4, 4)
>>> 
"""

import itertools # for count
import numbers # for Integral 


def is_in_range(x, start, stop = None, step = 1):
    """
    A naive implementation would be

    if stop is None:
         start, stop = 0, start
    return x in range(start, stop, step)
    
    However, 

    numpy.int64(1_000_000_000) in range(10_000_000_000) 

    takes forever.

    >>> all(is_in_range(x, stop) for x, stop in [(5, 8), (0, 5), (3, 4)])
    True
    >>> any(is_in_range(x, stop) for x, stop in [(8, 5), (-1, 3), (4, 4), (-10, 0), (-2, - 1)])
    False
    >>> all(is_in_range(x, start, stop) for x, start, stop in [(3, 2, 8), (3, 3, 4), (1, -1, 2)])
    True
    >>> any(is_in_range(x, start, stop) for x, start, stop in [(0, 2, 8), (4, -3, 4), (8, 2, 5)])
    False
    >>> all(is_in_range(x, start, stop, step) for x, start, stop, step in [(9, 1, 15, 4), (0, 8, -3, -2)])
    True
    >>> any(is_in_range(x, start, stop, step) for x, start, stop, step in [(2, 1, 9, 2), (7, 2, 7, 2), (-6, 1, -10, - 3)])
    False
    """
    
    if step == 0: raise ValueError("is_in_range() arg 3 must not be zero")
    if not isinstance(x, numbers.Integral):
        return False
    if stop is None:
         start, stop = 0, start
    if step < 0:
        if not (stop < x <= start):
            return False
    else:
        if not (start <= x < stop):
            return False
    return (x - start) % step == 0


def segregate(T, p):
    """
    Input:
    T is a list (the class of T must supply __getitem__, __setitem__, and __len__) and
    p is a one-argument callable (the predicate).

    Output:
    The function permutates T and returns a non-negative integer n such that    
    all(p(t) for t in T[:n]) and not any(p(t) for t in T[n:]) 

    The time complexity is linear in len(T).
    If T then the predicate p is called exactly len(T) times.
    The space complexity is bounded.
    
    After executing 

    n = segregate(T, lambda x: is_in_range(x, len(T)))

    the FMNNI of T[:n] is the same as that of the original list T, 
    so we may alway assume that every element of T is a non-negative integer. 

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
    >>> T = [1, 1, 1, 0, 0, 0]; n = segregate(T, p); T
    [1, 1, 1, 0, 0, 0]
    >>> all(p(t) for t in T[:n]) and not any(p(t) for t in T[n:]) 
    True
    """
    
    if not T: return 0
    i = 0
    j = len(T) - 1
    while i < j:
        
        # invariants:
        assert all(p(t) for t in T[:i])
        assert not any(p(t) for t in T[j + 1:])
        
        if p(T[i]):
            i += 1
        else:
            T[i], T[j] = T[j], T[i]
            j -= 1
    return i + bool(p(T[i]))


def FMNNI_naive(T):
    """
    Input:
    T is any object that supports the in operator.

    If T == list(range(n)) for some positive integer n then the time complexity is quadratic in n.
    """
    
    return next(n for n in itertools.count() if n not in T)


def FMNNI_sort(T):
    """
    Input:
    T is a list.

    The time and space complexities are that of sorting T in place with python's timsort algorithm.
    The algorithm permutates T.
    """
    
    n = len(T)  
    T.sort(key = lambda x: x if is_in_range(x, n) else n)
    # from the docs: "The C implementation of Python makes the list appear empty for the duration"
    i = 0
    iterT = iter(T)
    while i in iterT:
        i += 1
    return i


def FMNNI_linear_linear(T):
    """
    Input:
    T is a list (T must be iterable and its class must supply __len__).   

    T is not modified.
    The time and space complexities are linear in len(T).
    """

    n = len(T)
    is_here = [False] * (n + 1) # is_here[n] serves as a sentinel
    for t in T:
        if is_in_range(t, n):
            is_here[t] = True

    # invariant:
    assert all(is_here[i] == (i in T) for i in range(n)) 

    i = 0
    while is_here[i]:
        i += 1
    return i

    
def FMNNI_linear_const(T):
    """
    Input:
    T is a list (the class of T must supply __getitem__, __setitem__, and __len__).   
 
    The algorithm permutates T.
    The time complexity is linear in len(T).
    The space complexity is bounded. 
    """

    n = len(T)
    for i in range(n):

        # invariant:
        assert all(T[j] == j for j in T[:i] if is_in_range(j, n))
        
        j = T[i]
        while is_in_range(j, n) and j != T[j]:

            # invariants:
            assert T[i] != i
            assert T[T[i]] != T[i]
            
            T[i] = T[j] # The number of fixed points does not decrease 
            T[j] = j    # The number of fixed points increases by one
            # T[i] and T[j] are swapped.
            j = T[i]

    # invariant:
    assert all(T[i] == i for i in T if is_in_range(i, n))
    
    i = 0
    while i < n and T[i] == i:
        i += 1
    return i

       
if __name__ == "__main__":
    print("Entering doctest mode !")
    import doctest
    doctest.testmod()   
