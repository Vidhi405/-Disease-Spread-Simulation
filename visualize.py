import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import numpy as np
from config import *
from simulation import SUSCEPTIBLE, INFECTED, RECOVERED

def plot_counts(history):
    infected_counts = []
    recovered_counts = []
    for grid in history:
        infected_counts.append(np.sum(grid == INFECTED))
        recovered_counts.append(np.sum(grid == RECOVERED))

    days = range(len(history))
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 5))
    plt.plot(days, infected_counts, label="Infected", color="red")
    plt.plot(days, recovered_counts, label="Recovered", color="green")
    plt.xlabel("Days")
    plt.ylabel("People")
    plt.title("Disease Spread Over Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/plots/infection_curve.png")
    plt.show()

def animate_grid(history):
    fig, ax = plt.subplots()
    cmap = plt.get_cmap("viridis", 3)
    im = ax.imshow(history[0], cmap=cmap, vmin=0, vmax=2)

    def update(frame):
        im.set_array(history[frame])
        ax.set_title(f"Day {frame}")
        return [im]

    ani = animation.FuncAnimation(fig, update, frames=len(history), interval=200, repeat=False)
    ani.save("results/animations/simulation.gif", writer="pillow")
    plt.show()
