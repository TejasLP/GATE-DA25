import math
import numpy as np

# -------------------------------------------------------------
# 1. Parameters from GATE DA 2025 Q1.2.28
# -------------------------------------------------------------
n = 100
p = 1.0 / 6.0
q = 1.0 - p  # 5/6

# -------------------------------------------------------------
# 2. Exact Binomial Theoretical Calculation
# -------------------------------------------------------------
# Complement event A^c: None of the 100 dice show a 1 (X = 0)
# P(X = 0) = (100 choose 0) * (1/6)^0 * (5/6)^100 = (5/6)^100
p_ac_binom = q**n
p_a_binom = 1.0 - p_ac_binom

# -------------------------------------------------------------
# 3. Gaussian (Normal) Approximation via CLT (No SciPy)
# -------------------------------------------------------------
mu = n * p                                # 100 / 6 ≈ 16.6667
sigma = math.sqrt(n * p * q)              # sqrt(500 / 36) ≈ 3.7268

# Standard Normal CDF using Python's math.erf:
# Phi(z) = 0.5 * (1 + erf(z / sqrt(2)))
def norm_cdf(x, loc=0.0, scale=1.0):
    z = (x - loc) / scale
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

# (a) Without continuity correction: P(X >= 1) ≈ 1 - P(X <= 0)
p_ac_gauss_uncorr = norm_cdf(0.0, loc=mu, scale=sigma)
p_a_gauss_uncorr = 1.0 - p_ac_gauss_uncorr

# (b) With 0.5 continuity correction: P(X >= 1) ≈ 1 - P(X <= 0.5)
p_ac_gauss_corr = norm_cdf(0.5, loc=mu, scale=sigma)
p_a_gauss_corr = 1.0 - p_ac_gauss_corr

# -------------------------------------------------------------
# 4. Comparison Output
# -------------------------------------------------------------
print("=== GATE DA 2025 Q1.2.28: Binomial vs Gaussian Comparison ===")
print(f"Parameters: n = {n}, p = 1/6, q = 5/6")
print(f"Gaussian Mean (mu) = {mu:.4f}, Std Dev (sigma) = {sigma:.4f}\n")

print(f"{'Method':<38} | {'P(A^c) [Zero 1s]':<18} | {'P(A) [At least one 1]':<22}")
print("-" * 84)
print(f"{'Binomial Theoretical: 1 - (5/6)^100':<38} | {p_ac_binom:<18.6e} | {p_a_binom:<22.12f}")
print(f"{'Gaussian CLT (Uncorrected, X <= 0)':<38} | {p_ac_gauss_uncorr:<18.6e} | {p_a_gauss_uncorr:<22.12f}")
print(f"{'Gaussian CLT (Corrected, X <= 0.5)':<38} | {p_ac_gauss_corr:<18.6e} | {p_a_gauss_corr:<22.12f}")

print("\n=== Absolute Error in P(A) (Binomial vs Gaussian) ===")
print(f"Uncorrected Gaussian Error : {abs(p_a_binom - p_a_gauss_uncorr):.6e}")
print(f"Corrected Gaussian Error   : {abs(p_a_binom - p_a_gauss_corr):.6e}")
