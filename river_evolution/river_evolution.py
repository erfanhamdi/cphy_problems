import numpy as np
import matplotlib.pyplot as plt
class River_Evolution:

    def __init__(self, n=100, m=50, random_state=0):
        """
        Initialize a river evolution object
        """
        self.random_state = random_state
        self.n = n
        self.m = m
        self._initialize_grid()
    
    def _initialize_grid(self):
        """
        Sample a random lattice for the river evolution simulation. This method should
        write new values to the self.grid and self.grid_filled attributes. Make sure
        to set the random seed inside this method.
        """
        # np.random.seed(self.random_state)
        self.grid = np.zeros((2, self.n+1, self.m))
        # Setting a flat surface
        self.grid[0, ...] = 1
        self.grid_history = self.grid.copy()

    def _percipate(self):
        """
        Add water to random grid cells
        """
        # Randomly select a cell to add water to
        i = np.random.randint(0, self.n)
        j = np.random.randint(0, self.m)
        # i, j = (1, 1)
        # Add water to the cell
        self.grid[1, i, j] += 1
        self.grid_history[]

    def _total_height(self):
        """
        Calculate the total height of the grid
        """
        return self.grid[0]+self.grid[1]

    def _evolve(self):
        
        # Calculate the total height of the grid
        # Randomly select a cell
        i = np.random.randint(0, self.n)
        j = np.random.randint(0, self.m)
        # Artificial i, j 
        # i, j = (1, 1)
        # Artificially percipated water
        # self.grid[1, i, j] = 1
        s = self._total_height()
        # Calculate the height of the cell
        h = s[i, j]
        # Calculate the height of the neighbors
        neighbors = [(i+1, j), (i, j-1), (i, j+1)]
        # Check if the cell is on the edge
        # if i == self.n-1 and h > 0:
        #     self.grid[1, i, j] -= 1
        if j == 0 :
            neighbors[1] = (i, -1)
        if j == self.m-1:
            neighbors[2] = (i, 0)
        else:
        # Check if the cell is higher than the neighbors and if so, flow water to the neighbors
            for neighbor in neighbors:
                h_n = s[neighbor]
                while h>h_n:
                    n, m = neighbor
                    self.grid[1, i, j] -= 1
                    self.grid[1, n, m] += 1
                    s = self._total_height()
                    h = s[i, j]

    def run(self, n_steps=100):
        """
        Run the river evolution simulation for n_steps
        """
        orig_map=plt.cm.get_cmap('Blues')
  
# reversing the original colormap using reversed() function
        reversed_map = orig_map.reversed()
        for i in range(n_steps):
            t = np.random.rand()
            if t < 0.5:
                self._percipate()
            # print(self.grid)
            self.grid_history[1, ...] += self.grid[1, ...]
            self._evolve()
            self.grid_history[1, ...] += self.grid[1, ...]
            # plt.imshow(self.grid[1, :-1, :], cmap = 'Blues')
            # plt.figure()
            # plt.imshow(self.grid_history[1, ...])
            # plt.savefig('river_evolution/figs/river_evolution_{:03d}.png'.format(i))
            # print(i)

        return self.grid[1]

if __name__ == "__main__":
    # Create a simulation object
    sim = River_Evolution(20, 50)
    # Run the simulation
    nsteps = 2_000
    sim.run(nsteps)
    print(sim.grid[:, :-1, :])
    plt.figure()
    plt.imshow(sim.grid[1, :-1, :], cmap='gist_yarg')
    plt.title("Last composition")
    plt.figure()
    plt.imshow(sim.grid_history[1, :-1 , :]/nsteps, cmap='gist_yarg')
    plt.title("Time_history")
    plt.show()


