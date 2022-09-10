import numpy as np
import matplotlib.pyplot as plt

class AbelianSandpile:

    def __init__(self, n=100, random_state=None):
        self.n = n
        np.random.seed(random_state) # Set the random seed
        self.grid = np.random.choice([0, 1, 2, 3], size=(n, n))
        # self.grid = np.random.choice([3], size=(n, n))
        self.history =[self.grid.copy()] # Why did we need to copy the grid?
        self.all_durations = list() # useful to keep track of the duration of toppling events

    def step(self):
        """
        Perform a single step of the sandpile model. Step corresponds a single sandgrain 
        addition and the consequent toppling it causes. 

        Returns: None
        """
        ########## YOUR CODE HERE ##########
        #
        #
        # My solution starts by dropping a grain, and then solving for all topple events 
        #  until the sandpile is stable. Watch your boundary conditions carefully.
        #
        # I'd recommend using a while loop for the toppling events
        # We will use absorbing boundary conditions: excess sand grains fall off the edges
        # of the grid.
        # In addition to updating self.grid, keep track of the topple durations in the 
        # instance variable self.all_durations
        #
        #
        ########## YOUR CODE HERE ##########
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
            self.grid[mask_history] = 0
            duration += 1
        self.all_durations.append(duration)

    # we use this decorator for class methods that don't require any of the attributes 
    # stored in self. Notice how we don't pass self to the method
    @staticmethod
    def check_difference(grid1, grid2):
        """Check the total number of different sites between two grids"""
        return np.sum(grid1 != grid2)

    
    def simulate(self, n_step):
        """
        Simulate the sandpile model for n_step steps.
        """
        ########## YOUR CODE HERE ##########
        #
        #
        # YOUR CODE HERE. You should use the step method you wrote above.
        #
        #
        ########## YOUR CODE HERE ##########
        for i in range(n_step):
            self.step()
            if self.check_difference(self.grid, self.history[-1]) > 0:
                self.history.append(self.grid.copy())
        return self.grid

if __name__ == "__main__":
# Run sandpile simulation
    model = AbelianSandpile(n=100, random_state=0)
    # model.step()
    plt.figure()
    plt.imshow(model.grid, cmap='gray')

    model.simulate(10000)
    plt.figure()
    plt.imshow(model.grid, cmap='gray')
    plt.title("Final state")




    # Compute the pairwise difference between all observed snapshots. This command uses list
    # comprehension, a zip generator, and argument unpacking in order to perform this task
    # concisely.
    all_events =  [model.check_difference(*states) for states in zip(model.history[:-1], model.history[1:])]
    # remove transients before the self-organized critical state is reached
    all_events = all_events[1000:]
    # index each timestep by timepoint
    all_events = list(enumerate(all_events))
    # remove cases where an avalanche did not occur
    all_avalanches = [x for x in all_events if x[1] > 1]
    all_avalanche_times = [item[0] for item in all_avalanches]
    all_avalanche_sizes= [item[1] for item in all_avalanches]
    all_avalanche_durations = [event1 - event0 for event0, event1 in zip(all_avalanche_times[:-1], all_avalanche_times[1:])]


    log_bins = np.logspace(np.log10(2), np.log10(np.max(all_avalanche_durations)), 50) # logarithmic bins for histogram
    vals, bins = np.histogram(all_avalanche_durations, bins=log_bins)
    plt.figure()
    plt.loglog(10**bins[:-1], vals, '.', markersize=10)
    plt.title('Avalanche duration distribution')
    plt.xlabel('Avalanche duration')
    plt.ylabel('Count')

    ## Visualize activity of the avalanches
    # Make an array storing all pairwise differences between the lattice at successive
    # timepoints
    all_diffs = np.abs(np.diff(np.array(model.history), axis=0))
    all_diffs[all_diffs > 0] = 1
    all_diffs = all_diffs[np.sum(all_diffs, axis=(1, 2)) > 1] # Filter to only keep big events
    most_recent_events = np.sum(all_diffs[-100:], axis=0)
    plt.figure(figsize=(5, 5))
    plt.imshow(most_recent_events)
    plt.title("Avalanch activity in most recent timesteps")

    all_diffs = np.abs(np.diff(np.array(model.history), axis=0))
    all_diffs = all_diffs[np.sum(all_diffs, axis=(1, 2)) > 1] # Filter to only keep big events

    # Use a trick to calculate the sliding cumulative sum
    activity_cumulative = np.cumsum(all_diffs, axis=0)
    activity_sliding = activity_cumulative[50:] - activity_cumulative[:-50]

    plt.figure(figsize=(5, 5))
    plt.imshow(activity_sliding[-1])
    activity_sliding2 = activity_sliding[-500:]
    vmin = np.percentile(activity_sliding2, 1)
    # vmin = 0
    vmax = np.percentile(activity_sliding2, 99.8)
    for i in range(len(activity_sliding2) - 1):
        
        
        out_path = "cphy/hw/private_dump/sandpile/frame" + str(i).zfill(4) + ".png"

        plt.figure()
        plt.imshow(activity_sliding2[i], vmin=vmin, vmax=vmax)

        ax = plt.gca()
        ax.set_axis_off()
        ax.xaxis.set_major_locator(plt.NullLocator())
        ax.yaxis.set_major_locator(plt.NullLocator())
        ax.set_aspect(1, adjustable='box')

        plt.savefig(out_path, bbox_inches='tight', pad_inches=0.0, dpi=300)
        plt.close() 

