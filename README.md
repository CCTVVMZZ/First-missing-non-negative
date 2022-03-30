# First-missing-non-negative

The project started from [this LeetCode puzzle](https://leetcode.com/problems/first-missing-positive/).
The aim is to implement in Python various solutions to the following optimization problem:

**Name**: First Missing Non-Negative Integer (FMNNI).  
**Input**: A container `T`.  
**Output**: The smallest non-negative integer that is not in `T`.  

For example, the FMNNI of `[-1, 0, 2, 0, "a", 3.5, "a", 1, 3, 0.1, 2]` is equal to `4`.
In general, the output is `next(n for n in itertools.count() if n not in T)`.
