# ============================================================
# Problem 1.2.32: Set Operations Trace
# ============================================================

A = {"this", "that"}
B = {"that", "other"}
C = {"other", "this"}

print(f"Initial: A={A}, B={B}, C={C}")
# Output:
# Initial: A={'that', 'this'}, B={'that', 'other'}, C={'this', 'other'}

iteration = 0
while "other" in C:
    iteration += 1
    print(f"\n--- Iteration {iteration} ---")

    # Step 1: Set difference
    if "this" in A:
        A, B, C = A - B, B - C, C - A
        print(f"After difference (if 'this' in A):")
        print(f"  A = {A}")
        print(f"  B = {B}")
        print(f"  C = {C}")
        # Iteration 1 Output:
        #   A = {'this'}
        #   B = {'that'}
        #   C = {'other'}
        # Iteration 2 Output:
        #   A = {'other'}
        #   B = {'this'}
        #   C = {'that'}

    # Step 2: Set union
    if "that" in B:
        A, B, C = C | A, A | B, B | C
        print(f"After union (if 'that' in B):")
        print(f"  A = {A}")
        print(f"  B = {B}")
        print(f"  C = {C}")
        # Iteration 1 Output:
        #   A = {'this', 'other'}
        #   B = {'this', 'that'}
        #   C = {'that', 'other'}
        # Iteration 2 Output:
        #   (Condition False: 'that' not in {'this'}, skipped)

print("\n--- Final State ---")
print(f"A = {A}")
print(f"B = {B}")
print(f"C = {C}")
print(f"'this' in A: {'this' in A}")
print(f"'this' in B: {'this' in B}")
print(f"'this' in C: {'this' in C}")
# Output:
# --- Final State ---
# A = {'other'}
# B = {'this'}
# C = {'that'}
# 'this' in A: False
# 'this' in B: True
# 'this' in C: False
# Correct Option: (b) Only B
