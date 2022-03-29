# First-missing-non-negative

The aim of the project is to implement in Python various solutions to the following optimization problem:

Name: First Missing Non-Negative Integer (FMNNI).

Input: A container `T`.

Output: The smallest non-negative integer that is not in `T`.

For example, the FMNNI of `[-1, 0, 2, 0, "a", 3.5, "a", 1, 0.1, 2]` is equal to `3`.
In general, the output is `min(n for n in itertools.count() if n not in T)`.
We show that FMNNI can be solved in O(`len(T)`) time and constant extra space,
provided that we may arbitrarily alter the order of T 

