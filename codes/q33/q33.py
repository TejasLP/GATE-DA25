import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Point sys.path directly to the CoordGeo folder inside codes/q33/
script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(script_dir / "CoordGeo"))

from plotting.funcs import label_pts


# Define the function f(x)
def f(x):
    return (x**3) / 3.0 + 3.5 * (x**2) + 10.0 * x + 133.0 / 2.0


# Domain interval x in [-8, 0]
x = np.linspace(-8, 0, 500)
y = f(x)

# Critical and boundary points
x_loc_max, y_loc_max = -5.0, f(-5.0)    # Local maximum (187/3 ≈ 62.33)
x_loc_min, y_loc_min = -2.0, f(-2.0)    # Local minimum (347/6 ≈ 57.83)
x_glob_max, y_glob_max = 0.0, f(0.0)    # Global maximum (133/2 = 66.50)
x_glob_min, y_glob_min = -8.0, f(-8.0)  # Global minimum (239/6 ≈ 39.83)

# Construct the 2x4 matrix G_v required by label_pts
G_v = np.array([
    [x_loc_max, x_glob_max, x_loc_min, x_glob_min],
    [y_loc_max, y_glob_max, y_loc_min, y_glob_min]
])

vert_labels = [
    f"Local Max\n$(-5, {y_loc_max:.2f})$",
    r"Global Max $\left(0, \frac{133}{2}\right)$",
    f"Local Min\n$(-2, {y_loc_min:.2f})$",
    f"Global Min\n$(-8, {y_glob_min:.2f})$",
]

# Plotting
plt.figure(figsize=(7, 4.5))

# Blue curve
plt.plot(
    x,
    y,
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

# Pad axes so labels at the boundary points (-8 and 0) don't clip the frame
plt.xlim(-9.2, 1.5)
plt.ylim(35, 73)

# Plot styling
plt.title(r"Extrema of $f(x)$ on $[-8, 0]$", fontsize=11)
plt.xlabel(r"$x$", fontsize=10)
plt.ylabel(r"$f(x)$", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(loc="lower right", fontsize=8.5)
plt.tight_layout()

# Navigate from codes/q33/ -> codes/ -> GATE-DA25/ -> figs/
output_dir = script_dir.parents[1] / "figs"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "q33_extrema.pdf"

plt.savefig(output_path, format="pdf", bbox_inches="tight")
plt.close()

print(f"Figure saved to: {output_path}")
