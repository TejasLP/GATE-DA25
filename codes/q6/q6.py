import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Resolve project root and figs directory paths relative to the script location
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parents[1]  # Adjust parents level based on your directory depth
fig_dir = project_root / "figs"
fig_dir.mkdir(parents=True, exist_ok=True)

# 1. Load data from the .dat file created by the C program
data = np.loadtxt("timing_results.dat", skiprows=1)
n = data[:, 0]
time_ms = data[:, 1]

# 2. Compute a theoretical O(n^2) scaling curve to compare against
# We scale it using the last data point to align the curves visually
c = time_ms[-1] / (n[-1] ** 2)
theoretical_curve = c * (n ** 2)

# 3. Create the plot
plt.figure(figsize=(10, 6))

# Experimentally obtained graph in stem plot format
markerline, stemlines, baseline = plt.stem(
    n, 
    time_ms, 
    linefmt='b-', 
    markerfmt='bo', 
    basefmt='k-', 
    label='Measured Time (Stem Plot)'
)
plt.setp(stemlines, linewidth=1.5)
plt.setp(markerline, markersize=6)

# Theoretical O(n^2) reference curve
plt.plot(n, theoretical_curve, 'r--', label='Theoretical $O(n^2)$ Curve', linewidth=2)

# Formatting the plot
plt.xlabel('Matrix Size ($n$)', fontsize=12)
plt.ylabel('Execution Time (ms)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=11)
plt.tight_layout()

# 4. Save the figure as a PDF inside the resolved figs directory
output_path = fig_dir / "timing_stem_plot.pdf"
plt.savefig(output_path, format="pdf", bbox_inches="tight")
plt.close()

print(f"Successfully saved PDF to {output_path}")
