import numpy as np

# Set parameters
p = 0.6  # Probability of success (Heads)
num_trials = 100_000  # Number of Monte Carlo experiments for high precision
n_values = [10, 50, 100, 500, 1000]  # Varying sample sizes n

np.random.seed(42)

print(f"=== MONTE CARLO SIMULATION (True p = {p}) ===")
print(f"{'n':>6} | {'E[p_hat] (Simulated)':>20} | {'Var(p_hat) (Simulated)':>22} | {'Var(p_hat) (Theoretical)':>24}")
print("-" * 80)

var_p_hat_list = []

for n in n_values:
    # Generate Bernoulli trials matrix of shape (num_trials, n)
    tosses = np.random.binomial(n=1, p=p, size=(num_trials, n))
    
    # Compute sample mean p_hat for each experiment: (1/n) * sum(X_i)
    p_hat = np.mean(tosses, axis=1)
    
    # Simulated statistics
    mean_p_hat = np.mean(p_hat)
    var_p_hat = np.var(p_hat, ddof=1)
    
    # Theoretical variance: p * (1 - p) / n
    var_p_hat_theoretical = (p * (1 - p)) / n
    var_p_hat_list.append(var_p_hat)
    
    print(f"{n:6d} | {mean_p_hat:20.6f} | {var_p_hat:22.6f} | {var_p_hat_theoretical:24.6f}")

print("=" * 80)

# ---------------------------------------------------------
# Statement Evaluations
# ---------------------------------------------------------

# Statement i: E[p_hat] = p
stmt_i = np.isclose(np.mean(p_hat), p, atol=1e-3)

# Statement ii: E[p_hat] = p / n
stmt_ii = np.isclose(np.mean(p_hat), p / n_values[-1], atol=1e-3)

# Statement iii: As n increases, variance of p_hat decreases
stmt_iii = all(var_p_hat_list[i] > var_p_hat_list[i + 1] for i in range(len(var_p_hat_list) - 1))

# Statement iv: Variance of p_hat does not depend on n
stmt_iv = np.isclose(var_p_hat_list[0], var_p_hat_list[-1], atol=1e-3)

print("\n=== STATEMENT EVALUATION ===")
print(f"i)   E[p_hat] = p                        : {stmt_i} (ALWAYS TRUE)")
print(f"ii)  E[p_hat] = p / n                    : {stmt_ii} (FALSE)")
print(f"iii) As n increases, Var(p_hat) decreases: {stmt_iii} (ALWAYS TRUE)")
print(f"iv)  Var(p_hat) does not depend on n     : {stmt_iv} (FALSE)")

print("-" * 50)
print("Correct Statement(s):")
correct_opts = []
if stmt_i: correct_opts.append("i")
if stmt_ii: correct_opts.append("ii")
if stmt_iii: correct_opts.append("iii")
if stmt_iv: correct_opts.append("iv")
print(f"-> {', '.join(correct_opts)}")
