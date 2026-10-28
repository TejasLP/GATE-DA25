import numpy as np

# Set random seed for reproducibility
np.random.seed(42)
n = 5

# 1. Generate random matrix A where each row sums to 1
A_raw = np.random.rand(n, n)
A = A_raw / A_raw.sum(axis=1, keepdims=True)

# 2. Compute B = A^3 - 2A^2 + A
A2 = A @ A
A3 = A2 @ A
B = A3 - 2 * A2 + A

# 3. Calculate the eigenvalues of B
eigenvalues = np.linalg.eigvals(B)

# 4. Check if 0 is an eigenvalue (within numerical tolerance)
tolerance = 1e-10
has_zero_eigenvalue = np.any(np.abs(eigenvalues) < tolerance)

print("Eigenvalues of B:")
for i, ev in enumerate(eigenvalues, 1):
    print(f"  lambda_{i} = {ev.real:.6f} + {ev.imag:.6f}j")

print(f"\nIs 0 an eigenvalue of B? {has_zero_eigenvalue}")

# 5. Conclude singularity
if has_zero_eigenvalue:
    print("\nConclusion: Since 0 is an eigenvalue of B, matrix B is singular.")
else:
    print("\nConclusion: 0 is not an eigenvalue of B, matrix B is non-singular.")
