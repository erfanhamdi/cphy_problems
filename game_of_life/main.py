import numpy as np
import matplotlib.pyplot as plt

class Game_of_Life:

    def __init__(self, n=100, initial_grid = None, random_state=None):
        if initial_grid is not None:
            self.grid = initial_grid
            self.n = initial_grid.shape[0]-1
        else:
            self.n = n
            np.random.seed(random_state) # Set the random seed
            self.grid = np.random.choice([0, 1], size=(n+1, n+1))
        self.new_grid = self.grid.copy()

    def get_neighbors(self, i, j):
        """
        Get the neighbors of a given cell
        """
        neighbors = [(i+1, j), (i, j-1), (i, j+1), (i-1, j), (i+1, j+1), (i+1, j-1), (i-1, j+1), (i-1, j-1)]
        return neighbors
    
    def check_live_or_dead(self, i, j):
        """
        Check if a cell is alive or dead
        """
        if self.grid[i, j] == 1:
            return True
        else:
            return False
    
    def count_live_dead_on_neighbor_list(self, neighbor_list):
        """
        Check if a cell is alive or dead
        """
        sum_live = 0
        for neighbor in neighbor_list:
            if self.check_live_or_dead(neighbor[0], neighbor[1]) and neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < self.n and neighbor[1] < self.n:
                sum_live += 1
        return sum_live

    def step(self):
        for i in range(self.n):
            for j in range(self.n):
                neighbor_list = self.get_neighbors(i, j)
                sum_live = self.count_live_dead_on_neighbor_list(neighbor_list)
                alive = self.check_live_or_dead(i, j)
                if alive and sum_live == 3 or alive and sum_live == 2:
                    self.new_grid[i, j] = 1
                elif sum_live < 2 or sum_live > 3:
                    self.new_grid[i, j] = 0
                elif not alive and sum_live == 3:
                    self.new_grid[i, j] = 1
                else:
                    pass
        self.grid = self.new_grid.copy()
    
    def simulate(self, n_step):
        """
        Simulate the sandpile model for n_step steps.
        """
        for i in range(n_step):
            self.step()
            self.history.append(self.grid.copy())
            # plot the grid every 100 steps
            if i % 1 == 0:
                plt.figure()
                plt.imshow(self.grid, cmap='gray')
                plt.title(f"Step {i}")
                # save images to disk
                plt.savefig(f"figs/step_{i}.png")
                # close the figure
                plt.close()
        return self.grid

if __name__ == "__main__":
    # a glider
    glider = np.array([[0, 1, 0],
                        [0, 0, 1],
                        [1, 1, 1]])
    # initial grid with gliders and explosions
    initial_grid = np.zeros((25, 25))
    initial_grid[0:3, 0:3] = glider
    initial_grid[5:8, 1:4] = glider
    initial_grid[1:4, 13:16] = glider
    initial_grid[5:8, 13:16] = glider
    initial_grid[3, 14] = 1
    model = Game_of_Life(n=9, initial_grid = initial_grid, random_state=0)
    model.simulate(100)