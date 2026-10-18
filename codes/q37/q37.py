import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVC

# -------------------------------------------------------------
# 1. Resolve Project Root, CoordGeo, and Figures Directory
# -------------------------------------------------------------
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parents[1]  # Root directory (e.g., GATE-DA25/)
coordgeo_dir = project_root / "codes" / "CoordGeo"

# Add CoordGeo paths to sys.path
sys.path.insert(0, str(coordgeo_dir))
sys.path.insert(0, str(coordgeo_dir / "line"))
sys.path.insert(0, str(coordgeo_dir / "plotting"))

# Import custom CoordGeo functions
from line.funcs import line_gen
from plotting.funcs import label_pts

# Ensure root figs directory exists
fig_dir = project_root / "figs"
fig_dir.mkdir(parents=True, exist_ok=True)
output_path = fig_dir / "svm_hard_margin.pdf"

# -------------------------------------------------------------
# 2. Training Data (Column Vectors)
# -------------------------------------------------------------
x1 = np.array([[2.0], [0.0]])  # Class +1
x2 = np.array([[0.0], [2.0]])  # Class +1
x3 = np.array([[2.0], [2.0]])  # Class +1
x4 = np.array([[0.0], [0.0]])  # Class -1

X = np.hstack([x1, x2, x3, x4]).T  # Shape: (4, 2)
y = np.array([1.0, 1.0, 1.0, -1.0])

# -------------------------------------------------------------
# 3. Analytical Verification of w and b
# -------------------------------------------------------------
w_analytical = np.array([[1.0], [1.0]])
b_analytical = -1.0

# Functional margins: y_i * (w^T * x_i + b)
functional_margins = y * (X @ w_analytical + b_analytical).flatten()
is_feasible = np.all(functional_margins >= 1.0 - 1e-9)

# Support vectors lie on the canonical margin boundary (margin == 1)
sv_indices = np.where(np.isclose(functional_margins, 1.0))[0]
norm_w = np.linalg.norm(w_analytical)
margin_width = 2.0 / norm_w

# Classification accuracy
predictions = np.sign(X @ w_analytical + b_analytical).flatten()
accuracy = np.mean(predictions == y) * 100.0

print("=== Analytical Solution Verification ===")
print(f"w: {w_analytical.flatten()}")
print(f"b: {b_analytical}")
print(f"Functional Margins: {functional_margins}")
print(f"Feasibility Condition (>= 1): {is_feasible}")
print(f"Number of Support Vectors: {len(sv_indices)}")
print(f"Norm ||w||: {norm_w:.4f}")
print(
    f"Geometric Margin (2 / ||w||): {margin_width:.4f} (Exact: sqrt(2) = {np.sqrt(2):.4f})"
)
print(f"Training Accuracy: {accuracy:.1f}%\n")

# -------------------------------------------------------------
# 4. Numerical QP Solver Verification (Scikit-Learn Hard-Margin)
# -------------------------------------------------------------
clf = SVC(kernel="linear", C=1e9, tol=1e-9)
clf.fit(X, y)

print("=== Scikit-Learn Solver Verification ===")
print(f"w (solver): {np.round(clf.coef_[0], 4)}")
print(f"b (solver): {np.round(clf.intercept_[0], 4)}")
print(f"Number of Support Vectors: {len(clf.support_)}")

# -------------------------------------------------------------
# 5. Generate Lines using CoordGeo's line_gen
# -------------------------------------------------------------
# Decision boundary: x1 + x2 - 1 = 0
D1 = np.array([[-0.5], [1.5]])
D2 = np.array([[1.8], [-0.8]])
line_dec = line_gen(D1, D2)

# Positive margin (+1): x1 + x2 - 2 = 0
Mp1 = np.array([[-0.3], [2.3]])
Mp2 = np.array([[2.3], [-0.3]])
line_pos = line_gen(Mp1, Mp2)

# Negative margin (-1): x1 + x2 = 0
Mn1 = np.array([[-0.8], [0.8]])
Mn2 = np.array([[1.2], [-1.2]])
line_neg = line_gen(Mn1, Mn2)

# Convex hull edges of Class-1
tri_12 = line_gen(x1, x2)
tri_23 = line_gen(x2, x3)
tri_31 = line_gen(x3, x1)

# -------------------------------------------------------------
# 6. Plotting & Formatting
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 7))

# Plot lines generated via CoordGeo
ax.plot(
    line_dec[0, :],
    line_dec[1, :],
    color="black",
    lw=2,
    label=r"Decision Boundary: $\mathbf{w}^\top \mathbf{x} + b = 0$",
)
ax.plot(
    line_pos[0, :],
    line_pos[1, :],
    "b--",
    lw=1.5,
    label=r"$+1$ Margin: $\mathbf{w}^\top \mathbf{x} + b = 1$",
)
ax.plot(
    line_neg[0, :],
    line_neg[1, :],
    "r--",
    lw=1.5,
    label=r"$-1$ Margin: $\mathbf{w}^\top \mathbf{x} + b = -1$",
)

# Plot Class-1 triangle edges
ax.plot(tri_12[0, :], tri_12[1, :], "b:", alpha=0.5)
ax.plot(tri_23[0, :], tri_23[1, :], "b:", alpha=0.5)
ax.plot(tri_31[0, :], tri_31[1, :], "b:", alpha=0.5)

# Scatter data points
ax.scatter(
    X[:3, 0], X[:3, 1], color="blue", s=80, zorder=5, label="Class-1 (+1)"
)
ax.scatter(
    X[3:, 0], X[3:, 1], color="red", s=80, zorder=5, label="Class-2 (-1)"
)

# Highlight support vectors (x1, x2, x4)
sv_points = X[sv_indices]
ax.scatter(
    sv_points[:, 0],
    sv_points[:, 1],
    s=220,
    facecolors="none",
    edgecolors="green",
    lw=2,
    zorder=6,
    label="Support Vectors (3)",
)

# Annotate points using CoordGeo's label_pts
pts_block = np.block([x1, x2, x3, x4])
labels = [
    r"$\mathbf{x}_1(2,0)$",
    r"$\mathbf{x}_2(0,2)$",
    r"$\mathbf{x}_3(2,2)$",
    r"$\mathbf{x}_4(0,0)$",
]
label_pts(pts_block, labels)

# Formatting: Extra headroom so the legend clears (2, 2)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-1.0, 3.0)
ax.set_ylim(-1.0, 3.4)
ax.set_xlabel(r"$x_1$")
ax.set_ylabel(r"$x_2$")
ax.axhline(0, color="gray", lw=0.6, linestyle=":")
ax.axvline(0, color="gray", lw=0.6, linestyle=":")
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(loc="upper right", framealpha=0.95)

# Save directly to root figs/ directory
plt.tight_layout()
plt.savefig(output_path, format="pdf", bbox_inches="tight")
plt.close()
