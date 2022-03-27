def is_in_range(start, stop=None, step = 1):
    """
    A naive implementation would be:
    return lambda x: x in range(start, stop, step)
    """
    
    def wrapped(x):
        try:
            x = x.__index__()
        except AttributeError:
            return False
        if type(x) is not int: return False
        q, r = divmod(x - start, step)
        if r != 0: return False
        if step > 0:
            return x < stop
        return x > stop
        
    if step == 0: raise ValueError("is_in_range() arg 3 must not be zero")
    if stop is None:
         start, stop = 0, start
    return lambda x: (type(x) is int) and (x - start) % step 

def test(T: list) -> bool:
    return all(T[i] == i for i in T if type(i) is int and 0 <= i < len(T))
    

def swap(T: list, i: int, j: int) -> None:
    T[i], T[j] = T[j], T[i]


def toto(T: list) -> None:
    for i in range(len(T)):
        assert all(T[j] == j for j in T[:i] if type(j) is int and 0 <= j < len(T)) # Invariant
        j = T[i]
        while type(j) is int and 0 <= j < len(T) and j != T[j]:
            assert T[i] != i and T[T[i]] != T[i] # Invariant
            # Swapping T[i] and T[j] ...
            T[i] = T[j] # The number of fixed points does not decrease 
            T[j] = j    # The number of fixed points increases by one
            # ... T[i] and T[j] are swapped.
            j = T[i]

T1 = [1, 8, 6, 5, 7, -2, -11, 2, 14]
T2 = [1, 2, -8, 5, 7, 0, -11, 14]
T3 = [6, 3, 3, 2, 2, 5, 0, -1, 2, "za", 0, 1, -1, 12, 1, -3, 1]
T4 = list("azertrt") + [2] 
T5 = list(reversed([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))

for T in [T1, T2, T3, T4, T5]:
    print(maximum_fixed_points(T), T, end = " ")
    toto(T)
    print(maximum_fixed_points(T), T)
# for T in [T1, T2, T3, T4, T5]:
#     print(smallest_missing_nonnegative_integer(T), T)

# assert smallest_missing_nonnegative_integer([1, 2, -8, 5, 7, 0, -11, 14]) == 3
# assert smallest_missing_nonnegative_integer([-1, 3, 3, 2, 2, 5, 0, 6, 2, "za", 0, 1,  -1, 12, 1, -3, 1]) == 4
