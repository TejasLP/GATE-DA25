import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Resolve project root and CoordGeo paths relative to codes/q19/q19.py
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parents[1]  # GATE-DA25/
coordgeo_dir = project_root / "codes" / "CoordGeo"

# Add CoordGeo paths to sys.path
sys.path.insert(0, str(coordgeo_dir))
sys.path.insert(0, str(coordgeo_dir / "line"))
sys.path.insert(0, str(coordgeo_dir / "plotting"))

# Import custom functions from CoordGeo
from line.funcs import line_gen
from plotting.funcs import label_pts

# Resolve the root figs directory
fig_dir = project_root / "figs"
fig_dir.mkdir(parents=True, exist_ok=True)

# Define parameter t (derived from median = 3)
t = 2.0

# --- Generate CDF components using line_gen ---
# Flat region for x <= t
x_cdf_left = np.linspace(0, t, 200)
y_cdf_left = np.zeros_like(x_cdf_left)

# Sloped region for t <= x <= 4 using line_gen(A, B)
A_cdf = np.array([[t], [0.0]])
B_cdf = np.array([[4.0], [1.0]])
cdf_seg = line_gen(A_cdf, B_cdf)

# Flat region for x >= 4
x_cdf_right = np.linspace(4, 6, 200)
y_cdf_right = np.ones_like(x_cdf_right)

# --- Generate PDF components using line_gen ---
# Zero region for x < t
x_pdf_left = np.linspace(0, t, 200)
y_pdf_left = np.zeros_like(x_pdf_left)

# Constant region for t <= x <= 4 using line_gen(A, B)
A_pdf = np.array([[t], [0.5]])
B_pdf = np.array([[4.0], [0.5]])
pdf_seg = line_gen(A_pdf, B_pdf)

# Zero region for x > 4
x_pdf_right = np.linspace(4, 6, 200)
y_pdf_right = np.zeros_like(x_pdf_right)

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

# Plot CDF parts
ax1.plot(x_cdf_left, y_cdf_left, color="blue", lw=2)
ax1.plot(cdf_seg[0, :], cdf_seg[1, :], color="blue", lw=2, label="CDF segment")
ax1.plot(x_cdf_right, y_cdf_right, color="blue", lw=2)
ax1.set_title("Cumulative Distribution Function (CDF)")
ax1.set_xlabel("$x$")
ax1.set_ylabel("$F_X(x)$")
ax1.set_ylim(-0.1, 1.1)
ax1.grid(True)
ax1.legend()

# Annotate median using label_pts
plt.sca(ax1)
G_v_median = np.array([[3.0], [0.5]])
label_pts(G_v_median, [r"Median $(3, 0.5)$"])
ax1.scatter(3.0, 0.5, color="black", zorder=5)

# Plot PDF parts
ax2.plot(x_pdf_left, y_pdf_left, color="red", lw=2)
ax2.plot(
    pdf_seg[0, :], pdf_seg[1, :], color="red", lw=2, label="PDF height = 0.5"
)
ax2.plot(x_pdf_right, y_pdf_right, color="red", lw=2)
ax2.set_title("Probability Density Function (PDF)")
ax2.set_xlabel("$x$")
ax2.set_ylabel("$f_X(x)$")
ax2.set_ylim(-0.1, 0.8)
ax2.grid(True)
ax2.legend()

# Save PDF directly into the root figs/ directory
plt.tight_layout()
output_path = fig_dir / "pdf_cdf_distribution.pdf"
plt.savefig(output_path, format="pdf", bbox_inches="tight")
plt.close()

print(f"Successfully saved PDF to {output_path}")
