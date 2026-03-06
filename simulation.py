import numpy as np
import random
from config import *

SUSCEPTIBLE = 0
EXPOSED     = 1   
INFECTED    = 2  
RECOVERED   = 3
DEAD        = 4
VACCINATED  = 5


def initialize_grid():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    days_in_state = np.zeros_like(grid) 
    incubation_period = np.zeros_like(grid)  

    total_cells = GRID_SIZE * GRID_SIZE
    num_vaccinated = int(total_cells * VACCINATION_RATE)
    all_positions = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
    random.shuffle(all_positions)
    for x, y in all_positions[:num_vaccinated]:
        grid[x, y] = VACCINATED

    susceptible_positions = all_positions[num_vaccinated:]
    for x, y in random.sample(susceptible_positions, min(INITIAL_INFECTED, len(susceptible_positions))):
        grid[x, y] = INFECTED
        days_in_state[x, y] = 1

    return grid, days_in_state, incubation_period


def get_neighbors(x, y):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] if USE_DISTANCING else \
                 [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            neighbors.append((nx, ny))
    return neighbors


def step(grid, days_in_state, incubation_period):
    new_grid = grid.copy()
    new_days = days_in_state.copy()
    new_incubation = incubation_period.copy()

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            state = grid[x, y]

            if state == INFECTED:
                for nx, ny in get_neighbors(x, y):
                    if grid[nx, ny] == SUSCEPTIBLE:
                        prob = INFECTION_PROB * 0.5 if USE_MASKS else INFECTION_PROB
                        if random.random() < prob:
                            new_grid[nx, ny] = EXPOSED
                            new_days[nx, ny] = 1
                            new_incubation[nx, ny] = random.randint(INCUBATION_TIME_MIN, INCUBATION_TIME_MAX)

                new_days[x, y] += 1
                if new_days[x, y] >= RECOVERY_TIME:
                    if random.random() < DEATH_RATE:
                        new_grid[x, y] = DEAD
                    else:
                        new_grid[x, y] = RECOVERED
                    new_days[x, y] = 0
            elif state == EXPOSED:
                new_days[x, y] += 1
                if new_days[x, y] >= incubation_period[x, y]:
                    new_grid[x, y] = INFECTED
                    new_days[x, y] = 1

    return new_grid, new_days, new_incubation


def run_simulation():
    grid, days_in_state, incubation_period = initialize_grid()
    history = []
    for _ in range(MAX_DAYS):
        grid, days_in_state, incubation_period = step(grid, days_in_state, incubation_period)
        history.append(grid.copy())
    return history