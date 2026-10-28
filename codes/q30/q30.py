import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

# Point sys.path to the sibling CoordGeo folder inside codes/
script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(script_dir.parent / "CoordGeo"))

from plotting.funcs import label_pts

# ---------------------------------------------------------
# 1. Symbolic Calculations using SymPy
# ---------------------------------------------------------
x_sym = sp.Symbol("x", real=True)

# Define symbolic function: f(x) = x^3/3 + 3.5*x^2 + 10*x + 133/2
f_sym = (x_sym**3) / 3 + sp.Rational(7, 2) * (x_sym**2) + 10 * x_sym + sp.Rational(133, 2)

# Compute first derivative f'(x) = x^2 + 7x + 10
df_sym = sp.diff(f_sym, x_sym)

# Find critical points by solving f'(x) = 0
critical_points = sp.solve(df_sym, x_sym)  # Returns [-5, -2]

# Filter critical points inside interval [-8, 0]
domain_min, domain_max = -8, 0
valid_crit_pts = [pt for pt in critical_points if domain_min <= pt <= domain_max]

# Compute second derivative f''(x) = 2x + 7 for local extrema classification
d2f_sym = sp.diff(df_sym, x_sym)

local_max_pts = []
local_min_pts = []

for pt in valid_crit_pts:
    second_deriv_val = d2f_sym.subs(x_sym, pt)
    val = float(f_sym.subs(x_sym, pt))
    if second_deriv_val < 0:
        local_max_pts.append((float(pt), val))
    elif second_deriv_val > 0:
        local_min_pts.append((float(pt), val))

# Boundary points
boundary_pts = [(domain_min, float(f_sym.subs(x_sym, domain_min))),
                (domain_max, float(f_sym.subs(x_sym, domain_max)))]

# Evaluate all candidate points to find global max and min
all_candidates = local_max_pts + local_min_pts + boundary_pts
x_glob_min, y_glob_min = min(all_candidates, key=lambda item: item[1])
x_glob_max, y_glob_max = max(all_candidates, key=lambda item: item[1])

x_loc_max, y_loc_max = local_max_pts[0]
x_loc_min, y_loc_min = local_min_pts[0]

# ---------------------------------------------------------
# 2. Plotting the Results
# ---------------------------------------------------------
# Numerical function evaluation for plotting curve
f_num = sp.lambdify(x_sym, f_sym, "numpy")
x_vals = np.linspace(-8, 0, 500)
y_vals = f_num(x_vals)

# Construct the 2x4 matrix G_v required by label_pts
G_v = np.array(
    [
        [x_loc_max, x_glob_max, x_loc_min, x_glob_min],
        [y_loc_max, y_glob_max, y_loc_min, y_glob_min],
    ]
)

vert_labels = [
    f"Local Max\n$(-5, {y_loc_max:.2f})$",
    r"Global Max $\left(0, \frac{133}{2}\right)$",
    f"Local Min\n$(-2, {y_loc_min:.2f})$",
    f"Global Min\n$(-8, {y_glob_min:.2f})$",
]

plt.figure(figsize=(7, 4.5))

# Blue curve
plt.plot(
    x_vals,
    y_vals,
    color="blue",
    linewidth=1.8,
    label=r"$f(x) = \frac{x^3}{3} + \frac{7}{2}x^2 + 10x + \frac{133}{2}$",
)

# Red extrema points
plt.scatter(
    G_v[0, :],
    G_v[1, :],
    color="red",
    s=50,
    zorder=5,
    label="Extrema Points",
)

# Label extrema points using label_pts from CoordGeo/plotting/funcs.py
label_pts(G_v, vert_labels)

# Pad axes so labels at boundary points (-8 and 0) don't clip the frame
plt.xlim(-9.2, 1.5)
plt.ylim(35, 73)

# Plot styling
plt.title(r"Extrema of $f(x)$ on $[-8, 0]$", fontsize=11)
plt.xlabel(r"$x$", fontsize=10)
plt.ylabel(r"$f(x)$", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(loc="lower right", fontsize=8.5)
plt.tight_layout()

# Save figure to PDF
output_dir = script_dir.parents[1] / "figs"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "q30_extrema.pdf"

plt.savefig(output_path, format="pdf", bbox_inches="tight")
plt.close()

print(f"Figure saved to: {output_path}")
