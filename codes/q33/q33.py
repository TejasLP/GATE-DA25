import numpy as np

# Set dimension n
n = 4

# ---------------------------------------------------------
# Construct a random orthogonal matrix A using QR decomposition
# ---------------------------------------------------------
np.random.seed(42)
Q, _ = np.linalg.qr(np.random.randn(n, n))
A = Q  # A satisfies A^T * A = I_n

# 1. Verify property: ||A x||^2 == ||x||^2 for random vectors
x_test = np.random.randn(n)
norm_Ax_sq = np.linalg.norm(A @ x_test) ** 2
norm_x_sq = np.linalg.norm(x_test) ** 2
assert np.isclose(
    norm_Ax_sq, norm_x_sq
), "Property ||A x||^2 = ||x||^2 does not hold!"

# ---------------------------------------------------------
# Test Statements
# ---------------------------------------------------------

# Statement i: A must be orthogonal (A^T * A = I)
stmt_i = np.allclose(A.T @ A, np.eye(n))

# Statement ii: A = I is the ONLY solution
# Counterexample: Check if A can be -I or a Rotation Matrix (A != I)
stmt_ii_counterexample = not np.allclose(A, np.eye(n))
stmt_ii = not stmt_ii_counterexample  # False because non-identity orthogonal matrices exist

# Statement iii: Eigenvalues of A are either +1 or -1
# Counterexample: Real orthogonal matrices can have complex conjugate eigenvalues e^(i*theta)
# For instance, 2D Rotation matrix by 90 degrees (pi/2)
A_rot = np.array([[0, -1], [1, 0]])  # Orthogonal, ||A_rot x||^2 = ||x||^2
eigenvalues_rot = np.linalg.eigvals(A_rot)
stmt_iii = np.all(
    np.isclose(eigenvalues_rot, 1.0) | np.isclose(eigenvalues_rot, -1.0)
)

# Statement iv: A has full rank
rank_A = np.linalg.matrix_rank(A)
stmt_iv = rank_A == n

# ---------------------------------------------------------
# Output Results
# ---------------------------------------------------------
print("=== NUMERICAL RESULTS ===")
print(f"Norm condition test       : ||Ax||^2 = {norm_Ax_sq:.4f}, ||x||^2 = {norm_x_sq:.4f}")
print(f"Is A^T * A == I?         : {stmt_i}")
print(f"Rotation matrix eigenvalues: {eigenvalues_rot}")
print(f"Rank of A                : {rank_A} (Full rank = {n})")
print("-" * 50)

print("=== STATEMENT EVALUATION ===")
print(f"i)   A must be orthogonal               : {stmt_i} (ALWAYS TRUE)")
print(f"ii)  A = I is the only solution          : {stmt_ii} (FALSE: Counterexample A = -I or Rotation Matrix)")
print(f"iii) Eigenvalues of A are either +1 or -1: {stmt_iii} (FALSE: Counterexample 90° Rotation gives ±i)")
print(f"iv)  A has full rank                     : {stmt_iv} (ALWAYS TRUE)")

print("-" * 50)
print("Correct Statement(s):")
correct_opts = []
if stmt_i:
    correct_opts.append("i")
if stmt_ii:
    correct_opts.append("ii")
if stmt_iii:
    correct_opts.append("iii")
if stmt_iv:
    correct_opts.append("iv")
print(f"-> {', '.join(correct_opts)}")
