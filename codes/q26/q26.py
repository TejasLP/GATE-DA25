from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# 1. Project Root and Figures Directory (.pdf Output)
# -------------------------------------------------------------
try:
    script_dir = Path(__file__).resolve().parent
    # Check if project root is two levels up, otherwise fallback to script_dir
    project_root = script_dir.parents[1] if len(script_dir.parents) >= 2 else script_dir
except (NameError, IndexError):
    project_root = Path.cwd()

fig_dir = project_root / "figs"
fig_dir.mkdir(parents=True, exist_ok=True)
output_path = fig_dir / "q40_binomial_normal_clt.pdf"

# -------------------------------------------------------------
# 2. Parameters & Pure NumPy / Math Computations
# -------------------------------------------------------------
n = 300
theta = 0.25
mu = n * theta                                     # 75.0
sigma = math.sqrt(n * theta * (1 - theta))         # 7.5
a, b = 60, 90                                      # [mu - 2*sigma, mu + 2*sigma]

# Standard Normal CDF using math.erf: Phi(z) = 0.5 * (1 + erf(z / sqrt(2)))
def norm_cdf(x, loc=0.0, scale=1.0):
    z = (x - loc) / scale
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

# Normal PDF vectorized with NumPy
def norm_pdf(x, loc=0.0, scale=1.0):
    return (1.0 / (scale * math.sqrt(2.0 * math.pi))) * np.exp(-0.5 * ((x - loc) / scale)**2)

# Binomial PMF vectorized across an array of k values
def binomial_pmf(k_array, n_trials, p_val):
    return np.array([
        math.comb(n_trials, int(k)) * (p_val**int(k)) * ((1.0 - p_val)**(n_trials - int(k)))
        for k in k_array
    ])

# Domain ranges
k_vals = np.arange(45, 106)
binom_pmf = binomial_pmf(k_vals, n, theta)

x_smooth = np.linspace(45, 105, 500)
normal_pdf = norm_pdf(x_smooth, loc=mu, scale=sigma)

# Probabilities verification
target_k = np.arange(a, b + 1)
prob_exact_binom = np.sum(binomial_pmf(target_k, n, theta))
prob_clt_uncorrected = norm_cdf(2.0) - norm_cdf(-2.0)

# Fixed: Pass arguments cleanly into norm_cdf
prob_clt_corrected = norm_cdf(b + 0.5, loc=mu, scale=sigma) - norm_cdf(a - 0.5, loc=mu, scale=sigma)

print("=== GATE DA 2025 Q1.2.26 Verification (Pure NumPy/Math) ===")
print(f"Mean (mu)                  = {mu:.2f}")
print(f"Std Dev (sigma)            = {sigma:.4f}")
print(f"Exact Binomial P(60<=Y<=90): {prob_exact_binom:.6f}")
print(f"Standard CLT Phi(2)-Phi(-2): {prob_clt_uncorrected:.6f}")
print(f"Continuity-Corrected CLT   : {prob_clt_corrected:.6f}")

# -------------------------------------------------------------
# 3. Plotting and Vector PDF Export
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 5.5))

# Stem plot for discrete Binomial PMF
markerline, stemlines, baseline = ax.stem(
    k_vals,
    binom_pmf,
    linefmt="C0-",
    markerfmt="C0o",
    basefmt="C0-",
    label=rf"Binomial PMF: $Y \sim \mathrm{{Bin}}({n}, {theta})$",
)
plt.setp(stemlines, linewidth=1.2, alpha=0.85)
plt.setp(markerline, markersize=4.5)
plt.setp(baseline, linewidth=0.8, alpha=0.5)

# Smooth Normal PDF approximation
ax.plot(
    x_smooth,
    normal_pdf,
    color="C1",
    linewidth=2.2,
    zorder=5,
    label=rf"Normal PDF: $\mathcal{{N}}(\mu={mu:.0f}, \sigma^2={sigma**2:.2f})$",
)

# Shaded CLT target region [60, 90]
x_shade = np.linspace(a, b, 300)
ax.fill_between(
    x_shade,
    norm_pdf(x_shade, loc=mu, scale=sigma),
    color="C1",
    alpha=0.2,
    label=rf"CLT Interval ${a} \leq Y \leq {b}$: $\Phi(2) - \Phi(-2)$",
)

# Interval boundary markers at a = 60 and b = 90
ax.axvline(a, color="red", linestyle="--", linewidth=1.3, alpha=0.8)
ax.axvline(b, color="red", linestyle="--", linewidth=1.3, alpha=0.8)

# Aesthetics
ax.set_title(rf"Binomial PMF and Normal PDF Approximation ($n={n}, \theta={theta}$)")
ax.set_xlabel(r"$y$")
ax.set_ylabel("Probability / Density")
ax.set_xlim(45, 105)
ax.set_ylim(bottom=0)
ax.grid(True, linestyle="-", alpha=0.35)
ax.legend(loc="upper right", framealpha=0.95)

plt.tight_layout()

# Save vector PDF directly into fig_dir
plt.savefig(output_path, format="pdf", bbox_inches="tight")
plt.close(fig)

print(f"Successfully saved PDF to: {output_path.resolve()}")
