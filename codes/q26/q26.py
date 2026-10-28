from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom, norm

# -------------------------------------------------------------
# 1. Resolve Project Root and Figures Directory
# -------------------------------------------------------------
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parents[1]  # Root directory (e.g., GATE-DA25/)

fig_dir = project_root / "figs"
fig_dir.mkdir(parents=True, exist_ok=True)
output_path = fig_dir / "q40_binomial_normal_clt.pdf"

# -------------------------------------------------------------
# 2. Parameters from GATE DA 2025 Q1.2.26
# -------------------------------------------------------------
n = 300
theta = 0.25
mu = n * theta                        # 75.0
sigma = np.sqrt(n * theta * (1 - theta))  # 7.5
a, b = 60, 90                         # Interval [mu - 2*sigma, mu + 2*sigma]

# Plot window: [mu - 4*sigma, mu + 4*sigma] = [45, 105] so stems are clearly visible
k_vals = np.arange(45, 106)
binom_pmf = binom.pmf(k_vals, n, theta)

x_smooth = np.linspace(45, 105, 500)
normal_pdf = norm.pdf(x_smooth, loc=mu, scale=sigma)

# Verify numerical probabilities
prob_exact_binom = np.sum(binom.pmf(np.arange(a, b + 1), n, theta))
prob_clt_uncorrected = norm.cdf(2) - norm.cdf(-2)

print("=== GATE DA 2025 Q1.2.26 Verification ===")
print(f"Mean (mu) = {mu}, Std Dev (sigma) = {sigma}")
print(f"Exact Binomial P(60 <= Y <= 90) : {prob_exact_binom:.6f}")
print(f"CLT Approx phi(2) - phi(-2)     : {prob_clt_uncorrected:.6f}")

# -------------------------------------------------------------
# 3. Plotting (Matching Reference Style)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 5.5))

# Binomial PMF stem plot
markerline, stemlines, baseline = ax.stem(
    k_vals,
    binom_pmf,
    linefmt="C0-",
    markerfmt="C0o",
    basefmt="C0-",
    label=r"Binomial PMF: $Y \sim \mathrm{Bin}(300, 0.25)$",
)
plt.setp(stemlines, linewidth=1.2, alpha=0.85)
plt.setp(markerline, markersize=4.5)
plt.setp(baseline, linewidth=0.8, alpha=0.5)

# Normal PDF smooth curve
ax.plot(
    x_smooth,
    normal_pdf,
    color="C1",
    lw=2.2,
    zorder=5,
    label=r"Normal PDF: $\mathcal{N}(\mu=75, \sigma^2=56.25)$",
)

# Shade the target CLT interval [60, 90]
x_shade = np.linspace(a, b, 300)
ax.fill_between(
    x_shade,
    norm.pdf(x_shade, loc=mu, scale=sigma),
    color="C1",
    alpha=0.2,
    label=r"CLT Interval $60 \leq Y \leq 90$: $\phi(2) - \phi(-2)$",
)

# Boundary indicator lines at a = 60 and b = 90
ax.axvline(a, color="red", linestyle="--", lw=1.3, alpha=0.8)
ax.axvline(b, color="red", linestyle="--", lw=1.3, alpha=0.8)

ax.set_title(r"Binomial PMF and Normal PDF Approximation ($n=300, \theta=0.25$)")
ax.set_xlabel(r"$y$")
ax.set_ylabel("Probability / Density")
ax.set_xlim(45, 105)
ax.grid(True, linestyle="-", alpha=0.35)
ax.legend(loc="upper right", framealpha=0.95)

plt.tight_layout()
plt.savefig(output_path, format="pdf", bbox_inches="tight")
plt.close()

print(f"Saved figure to {output_path}")
