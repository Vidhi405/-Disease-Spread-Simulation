import numpy as np
import random
from config import *

SUSCEPTIBLE=0
EXPOSED=1
INFECTED=2
RECOVERED=3
DEAD=4
VACCINATED=5

def initialize_grid():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    days_in_state=np.zeros_like(grid)
    incubation_period= np.zeros_like(grid)

    total_cells= GRID_SIZE*GRID_SIZE
    num_vaccinated=int(total_cells*VACCINATION_RATE)
    all_positions=[(x,y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
    random.shuffle(all_positions)
    for x,y in all_positions[:num_vaccinated]:
        grid[x,y]=VACCINATED
    
    susceptible_positions=all_positions[num_vaccinated:]
    for x,y in random.sample(susceptible_positions, min(INITIAL_INFECTED, len(susceptible_positions))):
        grid[x,y]=INFECTED
        days_in_state[x,y]=1
    return grid, days_in_state, incubation_period

def get_neighbour(x,y):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] if USE_DISTANCING else \
                 [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    
    neighbours=[]
    for dx,dy in directions:
        nx,ny=x+dx,y+dy
        if 0<=nx<GRID_SIZE and 0<=ny<GRID_SIZE:
            neighbours.append((nx,ny))
    return neighbours

def step(grid, days_in_state, incubation_periods):
    new_grid=grid.copy()
    