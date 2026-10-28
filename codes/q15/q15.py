import gc
import time
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------------------
# 1. Resolve Project Root and Figures Directory
# -------------------------------------------------------------
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parents[1]  # Root directory (e.g., GATE-DA25/)

fig_dir = project_root / "figs"
fig_dir.mkdir(parents=True, exist_ok=True)
output_path = fig_dir / "bsearch_worst_case.pdf"
dat_path = script_dir / "bsearch_data.dat"


# -------------------------------------------------------------
# 2. Pure Python Iterative Binary Search
# -------------------------------------------------------------
def binary_search(arr: list[int], n: int, target: int) -> int:
    low = 0
    high = n - 1
    while low <= high:
        mid = (low + high) >> 1
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# -------------------------------------------------------------
# 3. CPU Warm-Up & Worst-Case Timing Benchmark
# -------------------------------------------------------------
np.random.seed(42)

# Warm up the CPU frequency scaler and Python bytecode interpreter
warmup_arr = list(range(1000))
for _ in range(50000):
    binary_search(warmup_arr, 1000, 1001)

# Array sizes (n) spanning the steep initial climb and linear intervals
n_values = np.array([
    16, 64, 150, 300, 500,
    1000, 1500, 2000, 2500, 3000,
    3500, 4000, 4500, 5000, 5500,
    6000, 6500, 7000, 7500, 8000,
    8500, 9000, 9500, 10000
])

BATCHES = 7          # Take minimum across batches to filter OS interrupts
ITERS_PER_BATCH = 8000

obtained_time = []
log2_n = np.log2(n_values)

gc.disable()  # Prevent garbage collection spikes during timing

for n in n_values:
    # Generate n random integers in strictly increasing order
    arr = np.cumsum(np.random.randint(1, 10, size=n)).tolist()

    # Target > arr[-1] forces the rightmost path: exactly floor(log2(n)) + 1 steps
    target = arr[-1] + 1

    best_avg_ns = float("inf")
    for _ in range(BATCHES):
        start_ns = time.perf_counter_ns()
        for _ in range(ITERS_PER_BATCH):
            binary_search(arr, n, target)
        end_ns = time.perf_counter_ns()

        avg_ns = (end_ns - start_ns) / ITERS_PER_BATCH
        if avg_ns < best_avg_ns:
            best_avg_ns = avg_ns

    obtained_time.append(best_avg_ns)

gc.enable()

obtained_time = np.array(obtained_time)

# Export data to .dat file for record-keeping
np.savetxt(
    dat_path,
    np.column_stack((n_values, log2_n, obtained_time)),
    fmt=["%d", "%.4f", "%.4f"],
    delimiter="\t",
    header="n\tlog2(n)\ttime_ns",
)

# -------------------------------------------------------------
# 4. Fit Theoretical O(log n) Logarithmic Curve
# -------------------------------------------------------------
slope, intercept = np.polyfit(log2_n, obtained_time, 1)
theoretical_at_pts = slope * log2_n + intercept

# Dense linear grid so the red curve renders as a smooth logarithmic graph
n_smooth = np.linspace(n_values.min(), n_values.max(), 1000)
theoretical_smooth = slope * np.log2(n_smooth) + intercept

ss_res = np.sum((obtained_time - theoretical_at_pts) ** 2)
ss_tot = np.sum((obtained_time - np.mean(obtained_time)) ** 2)
r_squared = 1.0 - (ss_res / ss_tot)

print("=== Binary Search Worst-Case Complexity Verification (Python) ===")
print(f"Fitted Theoretical Model: T(n) = {slope:.2f} * log2(n) + ({intercept:.2f}) ns")
print(f"R^2 Goodness of Fit: {r_squared:.4f}")
print(f"Exported Data: {dat_path}")
print(f"Saved Plot: {output_path}\n")

# -------------------------------------------------------------
# 5. Plotting & Formatting
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))

# Blue stem plot for obtained empirical values
markerline, stemlines, baseline = ax.stem(
    n_values,
    obtained_time,
    linefmt="b-",
    markerfmt="bo",
    basefmt="k-",
    label="Obtained Time (Stem Plot)",
)
plt.setp(stemlines, linewidth=1.5)
plt.setp(markerline, markersize=6, zorder=4)
plt.setp(baseline, linewidth=0.8, alpha=0.6)

# Smooth red logarithmic curve for expected theoretical O(log n)
ax.plot(
    n_smooth,
    theoretical_smooth,
    color="red",
    linestyle="-",
    lw=2.2,
    zorder=5,
    label=r"Theoretical $O(\log n)$ (Expected)",
)

ax.set_xlabel(r"Array Size $n$ (Sorted Increasing Order)")
ax.set_ylabel("Worst-Case Execution Time (ns)")
ax.set_title(r"Worst-Case Binary Search: Theoretical $O(\log n)$ vs Obtained Time")
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(loc="lower right", framealpha=0.95)

# Save directly to root figs/ directory as PDF
plt.tight_layout()
plt.savefig(output_path, format="pdf", bbox_inches="tight")
plt.close()
