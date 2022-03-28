from typing import Callable, Any


def is_in_range(start: int, stop: int | None = None, step: int = 1):
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
    >>> any(is_in_range(start, stop, step)(x) for x, start, stop, step in [])
    False
    """
    
    def wrapped(x):
        if type(x) is not int:
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


def segregate(T: list, p: Callable[[Any], bool]) -> int:
    """
    >>> p = lambda x: bool(x)
    >>> T = []; segregate(T, p) == 0; T
    True
    []
    >>> T = [0]; s(T, p); T
    True
    [0]
    >>> T = [1]; s(T, p); T
    True
    [1]
    >>> T = [2, 2]; s(T, p); T
    True
    [2, 2]
    >>> T = [0, 0, 0]; s(T, p); T
    True
    [0, 0, 0]
    >>> T = [0, 1, 1, 0]; s(T, p); T
    True
    [1, 1, 0, 0]
    >>> T = [1, 0, 0, 1]; s(T, p); T
    True
    [1, 1, 0, 0]
    >>> T = [1, 1, 1, 0, 0]; s(T, p); T
    True
    [1, 1, 1, 0, 0]

    If T != [] then the predicate p is called exactly len(T) - 1 times.
    If segregate(T, p) == n then 
   """
    if not T:
        return 0
    i = 0
    j = len(T) - 1
    while i < j:
        if p(T[i]):
            i += 1
        else:
            T[i], T[j] = T[j], T[i]
            j -= 1
    return i
        
def test_segregate(T, p):
    n = segregate(T, p)
    s = sum(p(t) for t in T)  
    return (n + p(T[n]) == s) and all(p(T[i]) for i in range(s)) and not any(p(T[i]) for i in range(s + 1, len(T)))

p = lambda x: bool(x)
for T in [[0], [1], [2, 2], [0, 0, 0], [0, 1, 1, 0], [1, 0, 0, 1], [1, 1, 1, 0, 0]]:
    assert test_segregate(T, p)
    
    # print(T, end = " ")
    # n = segregate(T, p)
    # print(n + p(T[n]), sum(p(t) for t in T), T)

            
# def test(T: list) -> bool:
#     return all(T[i] == i for i in T if type(i) is int and 0 <= i < len(T))
    

# def swap(T: list, i: int, j: int) -> None:
#     T[i], T[j] = T[j], T[i]


# def toto(T: list) -> None:
#     for i in range(len(T)):
#         assert all(T[j] == j for j in T[:i] if type(j) is int and 0 <= j < len(T)) # Invariant
#         j = T[i]
#         while type(j) is int and 0 <= j < len(T) and j != T[j]:
#             assert T[i] != i and T[T[i]] != T[i] # Invariant
#             # Swapping T[i] and T[j] ...
#             T[i] = T[j] # The number of fixed points does not decrease 
#             T[j] = j    # The number of fixed points increases by one
#             # ... T[i] and T[j] are swapped.
#             j = T[i]

# T1 = [1, 8, 6, 5, 7, -2, -11, 2, 14]
# T2 = [1, 2, -8, 5, 7, 0, -11, 14]
# T3 = [6, 3, 3, 2, 2, 5, 0, -1, 2, "za", 0, 1, -1, 12, 1, -3, 1]
# T4 = list("azertrt") + [2] 
# T5 = list(reversed([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))

# for T in [T1, T2, T3, T4, T5]:
#     print(maximum_fixed_points(T), T, end = " ")
#     toto(T)
#     print(maximum_fixed_points(T), T)
# for T in [T1, T2, T3, T4, T5]:
#     print(smallest_missing_nonnegative_integer(T), T)

# assert smallest_missing_nonnegative_integer([1, 2, -8, 5, 7, 0, -11, 14]) == 3
# assert smallest_missing_nonnegative_integer([-1, 3, 3, 2, 2, 5, 0, 6, 2, "za", 0, 1,  -1, 12, 1, -3, 1]) == 4

if __name__ == "__main__":
    print("Doctest mode !")
    import doctest
    doctest.testmod()
