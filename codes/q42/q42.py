# Create empty stack S
S = []

# Set x = 0, flag = 0, sum = 0
x = 0
flag = 0
total_sum = 0

# Push x onto S
S.append(x)

while len(S) > 0:
    if flag == 0:
        x = x + 1
        S.append(x)
    if x == 8:
        flag = 1
    if flag == 1:
        x = S.pop()
        if x % 2 != 0:  # x is odd
            S.pop()
        # In pseudocode without braces, only the immediate next statement (Pop)
        # is controlled by the 'if'. This accumulation runs on every pop step:
        total_sum = total_sum + x

print(total_sum)

# Output:
# 24

# Execution Trace:
# ----------------------------------------------------------------------
# 1. Pushing phase (flag == 0):
#    Numbers 1 through 8 are incrementally pushed onto the stack.
#    Stack content when x reaches 8: S = [0, 1, 2, 3, 4, 5, 6, 7, 8].
#    Condition 'x == 8' triggers and sets flag = 1.
#
# 2. Popping phase (flag == 1):
#    - Step 1: Pop x = 8 (even)
#      Odd check is False -> no extra pop.
#      total_sum = 0 + 8 = 8
#      Stack remaining: [0, 1, 2, 3, 4, 5, 6, 7]
#
#    - Step 2: Pop x = 7 (odd)
#      Odd check is True  -> additionally pops 6.
#      total_sum = 8 + 7 = 15
#      Stack remaining: [0, 1, 2, 3, 4, 5]
#
#    - Step 3: Pop x = 5 (odd)
#      Odd check is True  -> additionally pops 4.
#      total_sum = 15 + 5 = 20
#      Stack remaining: [0, 1, 2, 3]
#
#    - Step 4: Pop x = 3 (odd)
#      Odd check is True  -> additionally pops 2.
#      total_sum = 20 + 3 = 23
#      Stack remaining: [0, 1]
#
#    - Step 5: Pop x = 1 (odd)
#      Odd check is True  -> additionally pops 0.
#      total_sum = 23 + 1 = 24
#      Stack remaining: [] (empty)
#
# Loop terminates because S is empty.
# Final output: 24
