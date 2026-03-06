import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import numpy as np
from config import *
from simulation import SUSCEPTIBLE, EXPOSED, INFECTED, RECOVERED, DEAD, VACCINATED

# Clear, intuitive colors for each state
STATE_COLORS = {
    SUSCEPTIBLE: "#A8D8EA",   # Light blue
    EXPOSED:     "#FFD166",   # Amber (exposed/incubating)
    INFECTED:    "#E63946",   # Red
    RECOVERED:   "#06D6A0",   # Green
    DEAD:        "#2D2D2D",   # Dark grey
    VACCINATED:  "#9B5DE5",   # Purple
}

# Build a colormap from our state colors
from matplotlib.colors import ListedColormap
CMAP = ListedColormap([STATE_COLORS[i] for i in range(6)])


def _count_states(history):
    """Return arrays of counts per state across all days."""
    counts = {state: [] for state in STATE_COLORS}
    for grid in history:
        for state in STATE_COLORS:
            counts[state].append(int(np.sum(grid == state)))
    return counts


def plot_counts(history):
    counts = _count_states(history)
    days = range(len(history))

    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    fig.suptitle("Disease Spread Simulation (SEIRD Model)", fontsize=14, fontweight="bold")

    ax = axes[0]
    labels = {
        SUSCEPTIBLE: ("Susceptible", STATE_COLORS[SUSCEPTIBLE]),
        EXPOSED:     ("Exposed",     STATE_COLORS[EXPOSED]),
        INFECTED:    ("Infected",    STATE_COLORS[INFECTED]),
        RECOVERED:   ("Recovered",   STATE_COLORS[RECOVERED]),
        DEAD:        ("Dead",        STATE_COLORS[DEAD]),
        VACCINATED:  ("Vaccinated",  STATE_COLORS[VACCINATED]),
    }
    for state, (label, color) in labels.items():
        lw = 2.5 if state == INFECTED else 1.8
        ax.plot(days, counts[state], label=label, color=color, linewidth=lw)

    ax.set_xlabel("Days", fontsize=11)
    ax.set_ylabel("Number of People", fontsize=11)
    ax.set_title("Epidemic Curves Over Time")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)

    ax2 = axes[1]
    stack_states = [VACCINATED, SUSCEPTIBLE, EXPOSED, INFECTED, RECOVERED, DEAD]
    stack_data   = [counts[s] for s in stack_states]
    stack_colors = [STATE_COLORS[s] for s in stack_states]
    stack_labels = [labels[s][0] for s in stack_states]

    ax2.stackplot(days, stack_data, labels=stack_labels, colors=stack_colors, alpha=0.85)
    ax2.set_xlabel("Days", fontsize=11)
    ax2.set_ylabel("Population", fontsize=11)
    ax2.set_title("Population State Breakdown Over Time")
    ax2.legend(loc="upper right", fontsize=8)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("results/plots/infection_curve.png", dpi=150)
    plt.show()
    print("Chart saved to results/plots/infection_curve.png")

    peak_infected = max(counts[INFECTED])
    peak_day = counts[INFECTED].index(peak_infected)
    total_dead = counts[DEAD][-1]
    total_recovered = counts[RECOVERED][-1]
    print(f"\n📊 Simulation Summary")
    print(f"   Peak infected:   {peak_infected} people on day {peak_day}")
    print(f"   Total recovered: {total_recovered}")
    print(f"   Total dead:      {total_dead}")


def animate_grid(history):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis("off")

    im = ax.imshow(history[0], cmap=CMAP, vmin=0, vmax=5, interpolation="nearest")

    legend_labels = ["Susceptible", "Exposed", "Infected", "Recovered", "Dead", "Vaccinated"]
    patches = [mpatches.Patch(color=STATE_COLORS[i], label=legend_labels[i]) for i in range(6)]
    ax.legend(handles=patches, loc="upper right", fontsize=7, framealpha=0.8)

    title = ax.set_title("Day 0", fontsize=12)

    def update(frame):
        im.set_array(history[frame])
        title.set_text(f"Day {frame + 1}")
        return [im, title]

    ani = animation.FuncAnimation(fig, update, frames=len(history), interval=150, repeat=False)
    ani.save("results/animations/simulation.gif", writer="pillow")
    plt.show()
    print("Animation saved to results/animations/simulation.gif")