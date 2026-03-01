import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__),'..'))

from simulation import run_simulation
from visualize import plot_counts, animate_grid

# Result files including plots and animations
os.makedirs("results/plots", exist_ok=True)
os.makedirs("results/animations", exist_ok=True)

print("Running COVID-19 Simulations...")
history = run_simulation()
plot_counts(history)
animate_grid(history)