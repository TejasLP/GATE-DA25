import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Define dimension n
n = 5

# 1. Generate a random vector x and normalize it so that x^T * x = 1
x = np.random.randn(n)
x = x / np.linalg.norm(x)  # Ensures x^T * x = 1

# 2. Construct matrix A = I_n + x * x^T
I_n = np.eye(n)
A = I_n + np.outer(x, x)

print(f"Dimension n: {n}")
print(f"Vector x norm squared (x^T * x): {np.dot(x, x):.4f}\n")

# --- Verify Options ---

# Option i: Rank of A is n
rank_A = np.linalg.matrix_rank(A)
opt_i_correct = (rank_A == n)
print(f"i) Rank of A is {n}: {opt_i_correct} (Computed rank = {rank_A})")

# Option ii: A is invertible (determinant != 0 or full rank)
det_A = np.linalg.det(A)
opt_ii_correct = (not np.isclose(det_A, 0.0))
print(f"ii) A is invertible: {opt_ii_correct} (Determinant = {det_A:.4f})")

# Option iii: 0 is an eigenvalue of A
eigenvalues_A = np.linalg.eigvalsh(A)
has_zero_eigenvalue = np.any(np.isclose(eigenvalues_A, 0.0))
opt_iii_correct = has_zero_eigenvalue
print(f"iii) 0 is an eigenvalue of A: {opt_iii_correct} (Eigenvalues of A: {np.round(eigenvalues_A, 4)})")

# Option iv: A^-1 has a negative eigenvalue
A_inv = np.linalg.inv(A)
eigenvalues_A_inv = np.linalg.eigvalsh(A_inv)
has_negative_eigenvalue = np.any(eigenvalues_A_inv < 0)
opt_iv_correct = has_negative_eigenvalue
print(f"iv) A^-1 has a negative eigenvalue: {opt_iv_correct} (Eigenvalues of A^-1: {np.round(eigenvalues_A_inv, 4)})")

print("\n--- Summary ---")
print("Correct options based on verification: (i) and (ii)")
