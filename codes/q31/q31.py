import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Generate a random 10x5 matrix and compute QR decomposition
# Q matrix will have 5 orthonormal columns in R^10
X_rand = np.random.randn(10, 5)
X, _ = np.linalg.qr(X_rand)  # X shape: (10, 5)

# Verify orthonormality: X^T * X = I_5
assert np.allclose(np.dot(X.T, X), np.eye(5)), "Vectors are not orthonormal!"

# Construct matrix A = sum_{i=1}^5 (x_i * x_i^T) = X * X^T
A = np.dot(X, X.T)  # Shape: (10, 10)

# Compute Eigenvalues & Singular Values
eigenvalues = np.sort(np.linalg.eigvalsh(A))[::-1]
singular_values = np.sort(np.linalg.svd(A, compute_uv=False))[::-1]
det_A = np.linalg.det(A)
rank_A = np.linalg.matrix_rank(A)

# Print Verification Results
print("=== NUMERICAL RESULTS ===")
print(f"Eigenvalues of A     : {np.round(eigenvalues, 4)}")
print(f"Singular values of A : {np.round(singular_values, 4)}")
print(f"Determinant of A     : {det_A:.4e}")
print(f"Rank of A            : {rank_A}")

print("\n=== VERIFICATION ===")
print(
    f"i)  Singular values are also eigenvalues? : {np.allclose(singular_values, eigenvalues)}"
)
print(
    f"ii) Singular values are either 0 or 1?   : {np.all(np.isclose(singular_values, 0) | np.isclose(singular_values, 1))}"
)
print(f"iii) Determinant of A is 1?              : {np.isclose(det_A, 1.0)}")
print(f"iv) A is invertible?                     : {rank_A == 10}")
