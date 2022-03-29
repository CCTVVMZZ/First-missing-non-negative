import itertools # for count
import numbers # for Integral 


def is_in_range(x, start, stop = None, step = 1):
    """
    A naive implementation would be

    if stop is None:
         start, stop = 0, start
    return x in range(start, stop, step)
    
    However, numpy.int64(1_000_000_000) in range(10_000_000_000) takes forever.

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

def FMNN_naive(T):
    """
    The time complexity is quadratic in len(T).  
    The space complexity is bounded.
    """
    return next(n for n in itertools.count() if n not in T) 

def FMNN_sort(T):
    """
    The time complexity is linearithmic in len(T).
    The space complexity is that of sorting T.
    The algorithm permutates T.
    """
    
    n = len(T)
    T.sort(key = lambda x: x if is_in_range(x, n) else n)
    n = 0
    it = iter(T)
    while n in it: n += 1
    return n


def FMNN_linear_linear(T):
    """
    T is not modified.
    The time complexity is linear in len(T).
    The space complexity is also linear in len(T).
    """
    
    is_here = [False] * (len(T) + 1)
    for t in T:
        if is_in_range(t, len(T)):
            is_here[t] = True
    n = 0
    while is_here[n]:
        n += 1
    return n
    
def FMNN_linear_const(T):
    """
    The algorithm permutates T.
    The time complexity is linear in len(T).
    The space complexity is bounded. 
    """
    
    for i in range(len(T)):
        assert all(T[j] == j for j in T[:i] if is_in_range(j, len(T))) # Invariant
        j = T[i]
        while is_in_range(j, len(T)) and j != T[j]:
            assert T[i] != i and T[T[i]] != T[i] # Invariant
            # Swapping T[i] and T[j] ...
            T[i] = T[j] # The number of fixed points does not decrease 
            T[j] = j    # The number of fixed points increases by one
            # ... T[i] and T[j] are swapped.
            j = T[i]
    assert all(T[j] == j for j in T if is_in_range(j, len(T))) # Invariant
    n = 0
    while n < len(T) and T[n] == n:
        n += 1
    return n
    
            
test_set = [[0, 1, 2, 3],
            [3, 2, 0, 1], 
            [7, 5, 8, 0, 3, "toto", 1, 15, 2, 5, 2, 0, 1, 5, "aze"], 
            ]

for T in test_set:
    print(FMNN_naive(T.copy())
          == FMNN_sort(T.copy())
          == FMNN_linear_linear(T.copy())
          == FMNN_linear_const(T.copy())
          )
        
if __name__ == "__main__":
    print("Entering doctest mode !")
    import doctest
    doctest.testmod()   
