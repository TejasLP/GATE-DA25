# ============================================================
# Problem 1.2.14: Python List Operations
# ============================================================

# (a) A.extend(B)
# Appends all elements of iterable B to the end of list A in-place.
A = [1, 2, 3]
B = [4, 5, 6]
A.extend(B)
print("a) A.extend(B):", A)
# Output:
# a) A.extend(B): [1, 2, 3, 4, 5, 6]


# (b) A.append(B)
# Appends the entire object B as a single nested element to list A.
A = [1, 2, 3]
B = [4, 5, 6]
A.append(B)
print("b) A.append(B):", A)
# Output:
# b) A.append(B): [1, 2, 3, [4, 5, 6]]


# (c) A.update(B)
# 'list' does not implement 'update'; update() is defined for sets and dicts.
A = [1, 2, 3]
B = [4, 5, 6]
try:
    A.update(B)
except AttributeError as e:
    print("c) A.update(B):", type(e).__name__, "-", e)
# Output:
# c) A.update(B): AttributeError - 'list' object has no attribute 'update'


# (d) A.insert(B)
# list.insert() requires two arguments: (index, object).
A = [1, 2, 3]
B = [4, 5, 6]
try:
    A.insert(B)
except TypeError as e:
    print("d) A.insert(B):", type(e).__name__, "-", e)
# Output:
# d) A.insert(B): TypeError - insert expected 2 arguments, got 1

# Note: Even if an index is supplied, it inserts B as a nested element:
A = [1, 2, 3]
A.insert(len(A), B)
print("   A.insert(len(A), B):", A)
# Output:
#    A.insert(len(A), B): [1, 2, 3, [4, 5, 6]]
