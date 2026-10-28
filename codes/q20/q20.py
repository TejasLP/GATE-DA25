import numpy as np

# 1. Define design vector X and target vector y
X = np.array([[-1], 
              [ 2], 
              [ 3]])

y = np.array([[ 1], 
              [-5], 
              [ 5]])

# 2. Compute normal equation components
XT_X = np.dot(X.T, X)
XT_y = np.dot(X.T, y)

# 3. Solve for optimal w using normal equations: w* = (X^T * X)^(-1) * X^T * y
w_normal = np.dot(np.linalg.inv(XT_X), XT_y)[0, 0]

# 4. Cross-verify using NumPy's built-in linear least-squares solver
w_lstsq, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)
w_builtin = w_lstsq[0, 0]

# --- Output Results ---
print(f"X^T * X = {XT_X[0, 0]}")
print(f"X^T * y = {XT_y[0, 0]}")
print(f"Computed w* (Normal Equations) : {w_normal:.6f} (Exact: 2/7 = {2/7:.6f})")
print(f"Computed w* (np.linalg.lstsq)  : {w_builtin:.6f}")

# Verification check
assert np.isclose(w_normal, 2 / 7), "Normal equation result does not match 2/7!"
assert np.isclose(w_builtin, 2 / 7), "Built-in lstsq result does not match 2/7!"
print("\nVERIFICATION SUCCESSFUL: Both methods match 2/7 (~0.285714)")
