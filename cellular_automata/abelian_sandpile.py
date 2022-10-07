import numpy as np
import matplotlib.pyplot as plt

class AbelianSandpile:
    """
    An Abelian sandpile model simulation. The sandpile is initialized with a random
    number of grains at each lattice site. Then, a single grain is dropped at a random
    location. The sandpile is then allowed to evolve until it is stable. This process
    is repeated n_step times.

    A single step of the simulation consists of two stages: a random sand grain is 
    dropped onto the lattice at a random location. Then, a set of avalanches occurs
    causing sandgrains to get redistributed to their neighboring locations.
    
    Parameters:
    n (int): The size of the grid
    grid (np.ndarray): The grid of the sandpile
    history (list): A list of the sandpile grids at each timestep
    all_durations (list): A list of the durations of each avalanche
    """

    def __init__(self, n=100, random_state=None):
        self.n = n
        np.random.seed(random_state) # Set the random seed
        self.grid = np.random.choice([0, 1, 2, 3], size=(n, n))
        self.history =[self.grid.copy()] # Why did we need to copy the grid?
        self.all_durations = list() # useful to keep track of the duration of toppling events


    def step(self):
        """
        Perform a single step of the sandpile model. Step corresponds a single sandgrain 
        addition and the consequent toppling it causes. 

        Returns: None
        """
        new_grain_loc = np.random.choice(self.n, size=2)
        self.grid[new_grain_loc[0], new_grain_loc[1]] += 1
        mask_1 = (self.grid == 4)*1
        duration = 0
        while np.sum(mask_1) != 0:
            mask_1 = (self.grid >= 4)*1
            mask_history = mask_1.copy().astype(bool)
            row_mask = np.zeros_like(mask_1) + mask_1
            col_mask = np.zeros_like(mask_1) + mask_1
            row_mask[1:, :] += mask_1[:-1, :]
            row_mask[:-1, :] += mask_1[1:, :]
            col_mask[:, 1:] += mask_history[:, :-1]
            col_mask[:, :-1] += mask_history[:, 1:]
            final_mask = row_mask + col_mask
            final_mask[mask_history] = 0
            self.grid += final_mask
            self.grid[mask_history] -= 4
            duration += 1
        self.all_durations.append(duration)

    @staticmethod
    def check_difference(grid1, grid2):
        """Check the total number of different sites between two grids"""
        return np.sum(grid1 != grid2)

    
    def simulate(self, n_step):
        """
        Simulate the sandpile model for n_step steps.
        """
        for i in range(n_step):
            self.step()
            if self.check_difference(self.grid, self.history[-1]) > 0:
                self.history.append(self.grid.copy())
        return self.grid

if __name__ == '__main__':

    model = AbelianSandpile(n=100, random_state=0)

    plt.figure()
    plt.imshow(model.grid, cmap='gray')

    model.simulate(1000)
    plt.figure()
    plt.imshow(model.grid, cmap='gray')
    plt.title("Final state")
    plt.show()