def f(a, b):
    if a == 0:
        return b
    if a % 2 == 1:
        return 2 * f((a - 1) / 2, b)
    return b + f(a - 1, b)


# Function call
result = f(15, 10)
print(result)

# Output:
# 160

# Call stack trace:
# f(15, 10) -> 2 * f(7.0, 10)
# f(7.0, 10) -> 2 * f(3.0, 10)
# f(3.0, 10) -> 2 * f(1.0, 10)
# f(1.0, 10) -> 2 * f(0.0, 10)
# f(0.0, 10) -> 10
# Unrolling:
# f(1.0, 10)  = 2 * 10  = 20
# f(3.0, 10)  = 2 * 20  = 40
# f(7.0, 10)  = 2 * 40  = 80
# f(15, 10)   = 2 * 80  = 160
