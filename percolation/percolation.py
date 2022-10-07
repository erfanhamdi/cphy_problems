import numpy as np
class PercolationSimulation:

    def __init__(self, n=100, p=0.5, grid=None, random_state=None):
        """
        Initialize a PercolationSimulation object.

        Args:
            n (int): number of rows and columns in the lattice
            p (float): probability of a site being blocked in the randomly-sampled lattice
            random_state (int): random seed for numpy's random number generator. Used to
                ensure reproducibility across random simulations. The default value of None
                will use the current state of the random number generator without resetting
                it.
        """

        self.random_state = random_state # the random seed

        # Initialize a random grid if one is not provided. Otherwise, use the provided
        # grid.
        if grid is None:
            self.n = n
            self.p = p
            self.grid = np.zeros((n, n))
            self._initialize_grid()
        else:
            assert len(np.unique(np.ravel(grid))) <= 2, "Grid must only contain 0s and 1s"
            self.grid = grid.astype(int)
            # override numbers if grid is provided
            self.n = grid.shape[0]
            self.p = 1 - np.mean(grid)

        self.grid_filled = np.copy(self.grid)

    def _initialize_grid(self):
        """
        Sample a random lattice for the percolation simulation. This method should
        write new values to the self.grid and self.grid_filled attributes. Make sure
        to set the random seed inside this method.

        This is a helper function for the percolation algorithm, and so we denote it 
        with an underscore in order to indicate that it is not a public method (it is 
        used internally by the class, but end users should not call it). In other 
        languages like Java, private methods are not accessible outside the class, but
        in Python, they are accessible but external usage is discouraged by convention.

        Private methods are useful for functions that are necessary to support the 
        public methods (here, our percolate() method), but which we expect we might need
        to alter in the future. If we released our code as a library, others might 
        build software that accesses percolate(), and so we should not alter the 
        input/outputs because it's a public method
        """
        np.random.seed(self.random_state)
        self.grid = np.random.choice([1, 0], size=(self.n, self.n), p=[1-self.p, self.p])
        self.grid = np.pad(self.grid, (1, 1), 'constant', constant_values = (0, 0))
        self.grid_filled = np.copy(self.grid)

    def _poll_neighbors(self, i, j):
        """
        Check whether there is a filled site adjacent to a site at coordinates i, j in 
        self.grid_filled. Respects boundary conditions.
        """
        enforced_boundary_grid = self.grid_filled >= 2
        return any([enforced_boundary_grid[i-1, j], enforced_boundary_grid[i, j+1], enforced_boundary_grid[i, j-1]])

    def _flow(self, rs):
        """
        Run a percolation simulation using recursion

        This method writes to the grid and grid_filled attributes, but it does not
        return anything. In other languages like Java or C, this method would return
        void
        """
        self.grid_filled[0, :] = 2
        for i in range(self.grid_filled.shape[0]):
            out_path = "private_dump/percolation/frame" + str(rs*53+i).zfill(4) + ".png"
            open_cells = np.where(self.grid_filled[i]==1)[0]
            if len(open_cells) != 0:
                for open_coords in open_cells:
                    if self._poll_neighbors(i, open_coords):
                        self.grid_filled[i, open_coords] += 1
                for invert_coords in open_cells[np.argsort(-open_cells)]:
                    if self._poll_neighbors(i, invert_coords):
                        self.grid_filled[i, invert_coords] += 1
            plt.figure()
            plot_percolation(self.grid_filled)
            plt.grid(False)
            plt.axis('off')

            plt.savefig(out_path, bbox_inches='tight', pad_inches=0.0)
            plt.close()
        

    def percolate(self, rs):
        """
        Initialize a random lattice and then run a percolation simulation. Report results
        """

        self._initialize_grid()
        self._flow(rs)
        self.grid_filled = self.grid_filled[1:-1, 1:-1]
        out_path = "private_dump/percolation/frame" + str((rs+1)*52).zfill(4) + ".png"
        plt.grid(False)
        plt.axis('off')

        if any(self.grid_filled[-1, :]>=2):
            plot_percolation_end(self.grid_filled, True)
            plt.grid(False)
            plt.axis('off')
            plt.savefig(out_path, bbox_inches='tight', pad_inches=0.0)
            plt.close('all')
            return True
        else:
            plot_percolation_end(self.grid_filled, False)
            plt.grid(False)
            plt.axis('off')
            plt.savefig(out_path, bbox_inches='tight', pad_inches=0.0)
            plt.close('all')
            return False

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
def plot_percolation(mat):
    """
    Plots a percolation matrix, where 0 indicates a blocked site, 1 indicates an empty 
    site, and 2 indicates a filled site
    """
    cvals  = [0, 1, 2]
    colors = [(0, 0, 0), (0.4, 0.4, 0.4), (0.372549, 0.596078, 1)]

    norm = plt.Normalize(min(cvals), max(cvals))
    tuples = list(zip(map(norm,cvals), colors))
    cmap = LinearSegmentedColormap.from_list("", tuples)
    plt.imshow(mat, cmap=cmap, vmin=0, vmax=2)
    plt.grid(False)
    plt.axis('off')

def plot_percolation_end(mat, status):
    """
    If percolated a it would turn the screen to green
    """
    cvals  = [0, 1, 2]
    if status:
        colors = [(0, 0, 0), (0.4, 0.4, 0.4), (0.0, 1, 0)]
    else:
        colors = [(0, 0, 0), (0.4, 0.4, 0.4), (1, 0, 0)]

    norm = plt.Normalize(min(cvals), max(cvals))
    tuples = list(zip(map(norm,cvals), colors))
    cmap = LinearSegmentedColormap.from_list("", tuples)
    plt.imshow(mat, cmap=cmap, vmin=0, vmax=2)
    plt.grid(False)
    plt.axis('off')


rs = 1234
for rs in range(0, 10):
    model = PercolationSimulation(n=50, random_state=rs, p=0.4)
    print(model.percolate(rs))
    plt.figure()
    plt.grid(False)
    plt.axis('off')

    plot_percolation(model.grid_filled)

# model = PercolationSimulation(n=20, random_state=rs, p=0.4)
# print(model.percolate())
# plt.figure()
# plot_percolation(model.grid_filled)

# model = PercolationSimulation(n=20, random_state=rs, p=0.6)
# print(model.percolate())
# plt.figure()
# plot_percolation(model.grid_filled)

# model = PercolationSimulation(n=20, random_state=rs, p=0.9)
# print(model.percolate())
# plt.figure()
# plot_percolation(model.grid_filled)
# # plt.show()


# # Import William's solution
# #from solutions.percolation import PercolationSimulation

# pvals = np.linspace(0, 1, 25) # control parameter for percolation phase transition
# n_reps = 200 # number of times to repeat the simulation for each p value

# all_percolations = list()
# for p in pvals:
#     print("Running replicate simulations for p = {}".format(p), flush=True)
#     all_replicates = list()
#     for i in range(n_reps):
#         # Initialize the model
#         model = PercolationSimulation(30, p=p)
#         all_replicates.append(model.percolate())
#     all_percolations.append(all_replicates)

# plt.figure()
# plt.plot(pvals, np.mean(np.array(all_percolations), axis=1))
# plt.xlabel('Average site occupation probability')
# plt.ylabel('Percolation probability')

# plt.figure()
# plt.plot(pvals, np.std(np.array(all_percolations), axis=1))
# plt.xlabel('Standard deviation in site occupation probability')
# plt.ylabel('Percolation probability')

# plt.show()


# # Just from curiousity, plot the distribution of cluster sizes at the percolation threshold
# # why does it appear to be bimodal?
# # all_cluster_sizes = list()
# # p_c = 0.407259
# # n_reps = 5000
# # for i in range(n_reps):
# #     model = PercolationSimulation(100, p=p_c)
# #     model.percolate()
# #     cluster_size = np.sum(model.grid_filled == 2)
# #     all_cluster_sizes.append(cluster_size)

# #     if i % 500 == 0:
# #         print("Finished simulation {}".format(i), flush=True)

# # all_cluster_sizes = np.array(all_cluster_sizes)

# # plt.figure()
# # plt.hist(all_cluster_sizes, 50)
# # plt.show()

# initial_lattice = np.zeros((50, 50))

# # Decide the order in which sites become blocked
# np.random.seed(0)
# all_lattice_indices = np.array(
#     [(i, j) for i in range(initial_lattice.shape[0]) for j in range(initial_lattice.shape[1])]
# )
# np.random.shuffle(all_lattice_indices)

# # does percolate 
# all_grids = list()
# for inds in all_lattice_indices:
    
#     initial_lattice[inds[0], inds[1]] = 1
#     model = PercolationSimulation(grid=initial_lattice)
#     model.percolate()

#     if (model.p > 0.3) and (model.p < 0.7):
#         all_grids.append(np.copy(model.grid_filled))

# for i in range(len(all_grids[::2]) - 1):
    
    
#     out_path = "private_dump/percolation/frame" + str(i).zfill(4) + ".png"

#     plt.figure()
#     plot_percolation(all_grids[::2][i])

#     ax = plt.gca()
#     ax.set_axis_off()
#     ax.xaxis.set_major_locator(plt.NullLocator())
#     ax.yaxis.set_major_locator(plt.NullLocator())
#     ax.set_aspect(1, adjustable='box')

#     plt.savefig(out_path, bbox_inches='tight', pad_inches=0.0, dpi=160)
#     plt.close()