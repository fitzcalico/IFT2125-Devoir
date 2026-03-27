print(f'Downloading modules...')
import time
import itertools
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import json
print(f'Downloading datasets...')
default_sample_sizes = [128, 64, 32, 16, 8, 4]
n_offset, n_base = 20, 2
default_n_grid = [n_offset * n_base ** (i) for i in range(len(default_sample_sizes))]
dataset = dict()
with open('datasets/dataset1.json') as f: dataset[default_n_grid[0]] = json.load(f)
with open('datasets/dataset2.json') as f: dataset[default_n_grid[1]] = json.load(f)
with open('datasets/dataset3.json') as f: dataset[default_n_grid[2]] = json.load(f)
with open('datasets/dataset4.json') as f: dataset[default_n_grid[3]] = json.load(f)
with open('datasets/dataset5.json') as f: dataset[default_n_grid[4]] = json.load(f)
with open('datasets/dataset6.json') as f: dataset[default_n_grid[5]] = json.load(f)
for n_iter, n in enumerate(default_n_grid):
    for sample_iter in range(default_sample_sizes[n_iter]):
        dataset[n][sample_iter] = np.array(dataset[n][sample_iter])
print(f'Downloads successful!')
default_minimum, default_maximum = -100.0, 100.0
default_decimals = 2
markers = ['o', 's', '^', 'D', 'v', 'P']
linestyles = ['-', '--', '-.', ':']
colors = ['green', 'red', 'blue', 'black', 'purple', 'orange']

def round_decimals(float_number, decimals=default_decimals):
    """
    Input:
        float_number: (float) Any float number we wish to truncate
        decimals: (int) Number of decimals to keep
    Output:
        truncated_float: (float) Truncated float_number
    """
    power = 10 ** decimals
    truncated_float = round(float_number * power) / power
    return truncated_float

def generate_problem_instance(n, minimum=None, maximum=None):
    """
    Input:
        n: (int) Number of vertices on each side of the bipartite graph
    Output:
        P: (numpy 2xnxn 3D array of floats) Uniform random set of preference scores within {min,max}ima constraints
    """
    if minimum is None: minimum = default_minimum
    if maximum is None: maximum = default_maximum
    P = np.random.uniform(low=minimum, high=maximum, size=(2, n, n))
    return P

def compute_matching_stability(matching, X, Y):
    """
    Input:
        matching: (list of 2-tuples of ints) Candidate matching
        X: (numpy nxn 2D array of floats) Uniform random set of preference scores
        Y: (numpy nxn 2D array of floats) Uniform random set of preference scores
    Output:
        stability: (float between 0 and 1) The ratio of pairs of couples in matching that are stable
    """
    pairs_of_couples, unstable_pairs_of_couples = 0, 0
    for ((i, j), (u, v)) in itertools.combinations(matching, 2):
        pairs_of_couples += 1
        is_unstable = (X[i][v] > X[i][j] and Y[v][i] > Y[v][u]) or (X[u][j] > X[u][v] and Y[j][u] > Y[j][i])
        unstable_pairs_of_couples += is_unstable
        #if is_unstable: print((i, j), (u, v), (X[i][v], X[i][j]), (Y[v][i], Y[v][u]), (X[u][j], X[u][v]), (Y[j][u], Y[j][i]))
    stability = (pairs_of_couples - unstable_pairs_of_couples) / pairs_of_couples
    return stability

def time_transformation(t):
    """
    Input:
        t: (float or np-array) Computation time(s) in microseconds
    Output:
        transformed_t: (float or np-array) Computation time(s) in log scale
    """
    return np.log10(1.0 + t)

def estimate_computation_times(algorithms, n_grid=default_n_grid, sample_sizes=None, verbose=True):
    """
    Input:
        algorithms: (list of StableMatchingAlgorithm objects) Algorithms that compute stable or near-stable matchings
        n_grid: (list of ints) The sizes of the problem instances to generate/load
        sample_sizes: (list of list of ints) The numbers of times a problem instance of a certain size is generated/loaded;
                                             possibly different for each algorithm
    Output:
        computation_times_means: (list of list of floats) Means of log-scale computation times for each algo and problem size
        computation_times_stds: (list of list of floats) Standard deviations of log-scale computation times for each algo and problem size
        objective_values_means: (list of list of floats) Means of objective values for each algo and problem size
        objective_values_stds: (list of list of floats) Standard deviations of objective values for each algo and problem size
    """
    if sample_sizes is None:
        sample_sizes = [default_sample_sizes for algo_iter in range(len(algorithms))]
    max_sample_sizes = []
    for n_iter, n in enumerate(n_grid):
        max_sample_size = 0
        for algo_iter in range(len(algorithms)):
            if n_iter < len(sample_sizes[algo_iter]):
                max_sample_size = max(max_sample_size, sample_sizes[algo_iter][n_iter])
        max_sample_sizes.append(max_sample_size)
    computation_times_means = [[0.0 for i in range(len(sample_sizes[algo_iter]))] for algo_iter in range(len(algorithms))]
    computation_times_stds = [[0.0 for i in range(len(sample_sizes[algo_iter]))] for algo_iter in range(len(algorithms))]
    computation_times = [[[] for i in range(len(sample_sizes[algo_iter]))] for algo_iter in range(len(algorithms))]
    objective_values_means = [[0.0 for i in range(len(sample_sizes[algo_iter]))] for algo_iter in range(len(algorithms))]
    objective_values_stds = [[0.0 for i in range(len(sample_sizes[algo_iter]))] for algo_iter in range(len(algorithms))]
    objective_values = [[[] for i in range(len(sample_sizes[algo_iter]))] for algo_iter in range(len(algorithms))]
    for n_iter, n in enumerate(n_grid):
        max_sample_size = max_sample_sizes[n_iter]
        if max_sample_size == 0: continue
        if verbose: print(f'Computing average computation times for n = {n}')
        for sample_iter in range(max_sample_size):
            if verbose and n_iter >= 3: print(f'\tRunning sample {sample_iter + 1}')
            if n in default_n_grid and sample_iter < default_sample_sizes[n_iter]: P = dataset[n][sample_iter]
            else: P = generate_problem_instance(n)
            for algo_iter, algorithm in enumerate(algorithms):
                if n_iter >= len(sample_sizes[algo_iter]): continue
                if sample_iter >= sample_sizes[algo_iter][n_iter]: continue
                start_time = time.perf_counter()
                score, matching = algorithm.solve(P)
                computation_time = time.perf_counter() - start_time
                computation_times[algo_iter][n_iter].append(1e6 * computation_time)
                objective_values[algo_iter][n_iter].append(score)
    for algo_iter in range(len(algorithms)):
        for n_iter in range(len(sample_sizes[algo_iter])):
            time_array = time_transformation(np.array(computation_times[algo_iter][n_iter]))
            objective_array = np.array(objective_values[algo_iter][n_iter])
            computation_times_means[algo_iter][n_iter] = np.mean(time_array)
            computation_times_stds[algo_iter][n_iter] = np.std(time_array)
            objective_values_means[algo_iter][n_iter] = np.mean(objective_array)
            objective_values_stds[algo_iter][n_iter] = np.std(objective_array)
    return computation_times_means, computation_times_stds, objective_values_means, objective_values_stds

def plot_computation_times(algorithms, identifier, computation_times_means, computation_times_stds, n_grid):
    """
    Input:
        algorithms: (list of StableMatchingAlgorithm objects) Algorithms that computed stable or near-stable matchings
        identifier: (string) Custom string for personalizing file names and paths
        computation_times_means: (list of list of floats) Means of log-scale computation times for each algo and problem size
        computation_times_stds: (list of list of floats) Standard deviations of log-scale computation times for each algo and problem size
        n_grid: (list of ints) The sizes of the problem instances that were generated/loaded
    Output:
        SAVED_FIGURE
    """
    log_n_grid = [math.log2(n // n_offset) for n in n_grid]
    for log_n_iter, log_n in enumerate(log_n_grid):
        if int(log_n) == log_n: log_n_grid[log_n_iter] = int(log_n)
    fig, ax = plt.subplots(figsize=(8, 6))
    for algo_iter, algorithm in enumerate(algorithms):
        means = np.array(computation_times_means[algo_iter])
        bars = 2 * np.array(computation_times_stds[algo_iter])
        ax.errorbar(log_n_grid[:len(means)], means, yerr=bars,
            linewidth=2, markersize=6, capsize=6, elinewidth=1,
            marker=markers[algo_iter % len(markers)], linestyle=linestyles[algo_iter % len(linestyles)],
            color=colors[algo_iter % len(colors)], label=algorithm.pretty_name)
    ax.legend(loc='best', frameon=False, fontsize=11, handlelength=3, handletextpad=0.5)
    ax.set_title(f'Influence of problem size ' + r'$n$' + ' over computation time', fontsize=14, pad=15)
    ax.set_xlabel(r'$\log_{2}(n / $' + f'{n_offset}' + r'$)$', fontsize=12)
    ax.set_ylabel(r'$\text{Average } \log_{10}(1 + \text{computation time [}\mu\text{s]})$', fontsize=12)
    ax.xaxis.labelpad = 10
    ax.yaxis.labelpad = 10
    ax.set_xticks(log_n_grid)
    ax.set_xticklabels([str(i) for i in log_n_grid], fontsize=10)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.grid(True, which='major', linestyle='--', linewidth=0.8, alpha=0.6)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    figure_directory = f'figures/{identifier}/'
    figure_name = f'ComputationTimes.png'
    plt.savefig(figure_directory + figure_name, dpi=600, bbox_inches='tight', transparent=False)
    print(f'Saved {figure_name} under {figure_directory}')
    plt.clf()

def plot_objective_values(algorithms, identifier, objective_values_means, objective_values_stds, n_grid):
    """
    Input:
        algorithms: (list of StableMatchinAlgorithm objects) Algorithms that computed stable or near-stable matchings
        identifier: (string) Custom string for personalizing file names and paths
        objective_values_means: (list of list of floats) Means of objective values for each algo and problem size
        objective_values_stds: (list of list of floats) Standard deviations of objective values for each algo and problem size
        n_grid: (list of ints) The sizes of the problem instances that were generated/loaded
    Output:
        SAVED_FIGURE
    """
    log_n_grid = [math.log2(n // n_offset) for n in n_grid]
    for log_n_iter, log_n in enumerate(log_n_grid):
        if int(log_n) == log_n: log_n_grid[log_n_iter] = int(log_n)
    fig, ax = plt.subplots(figsize=(8, 6))
    for algo_iter, algorithm in enumerate(algorithms):
        means = np.array(objective_values_means[algo_iter])
        bars = 2 * np.array(objective_values_stds[algo_iter])
        ax.errorbar(log_n_grid[:len(means)], means, yerr=bars,
            linewidth=2, markersize=6, capsize=6, elinewidth=1,
            marker=markers[algo_iter % len(markers)], linestyle=linestyles[algo_iter % len(linestyles)],
            color=colors[algo_iter % len(colors)], label=algorithm.pretty_name)
    ax.legend(loc='best', frameon=False, fontsize=11, handlelength=3, handletextpad=0.5)
    ax.set_title(f'Influence of problem size ' + r'$n$' + ' over stability', fontsize=14, pad=15)
    ax.set_xlabel(r'$\log_{2}(n / $' + f'{n_offset}' + r'$)$', fontsize=12)
    ax.set_ylabel(f'Stability', fontsize=12)
    ax.set_ylim(-0.025, 1.025)
    ax.xaxis.labelpad = 10
    ax.yaxis.labelpad = 10
    ax.set_xticks(log_n_grid)
    ax.set_xticklabels([str(i) for i in log_n_grid], fontsize=10)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.grid(True, which='major', linestyle='--', linewidth=0.8, alpha=0.6)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    figure_directory = f'figures/{identifier}/'
    figure_name = f'ObjectiveValues.png'
    plt.savefig(figure_directory + figure_name, dpi=600, bbox_inches='tight', transparent=False)
    print(f'Saved {figure_name} under {figure_directory}')
    plt.clf()

def compare_algorithms(algorithms, identifier, n_grid=default_n_grid, sample_sizes=default_sample_sizes, verbose=True):
    """
    Input:
        algorithms: (list of StableMatchinAlgorithm objects) Algorithms that compute stable or near-stable matchings
        identifier: (string) Custom string for personalizing file names and paths
        n_grid: (list of ints) The sizes of the problem instances to generate/load
        sample_sizes: (list of list of ints) The numbers of times a problem instance of a certain size is generated/loaded;
                                             possibly different for each algorithm
    Output:
        SAVED_FIGURE
    """
    ct_means, ct_stds, ov_means, ov_stds = estimate_computation_times(algorithms, n_grid, sample_sizes, verbose)
    plot_computation_times(algorithms, identifier, ct_means, ct_stds, n_grid)
    plot_objective_values(algorithms, identifier, ov_means, ov_stds, n_grid)

class StableMatchingAlgorithm:

    def __init__(self, pretty_name, symetric=False):
        self.pretty_name = f'{pretty_name}'
        self.is_symetric = symetric
    
    def process_input(self, P):
        """
        Input:
            P: (numpy 2xnxn 3D array of floats) Uniform random set of preference scores
        Output:
            X: (numpy nxn 2D array of floats) Uniform random set of preference scores for the men
            Y: (numpy nxn 2D array of floats) Uniform random set of preference scores for the women
            n: (int) Number of vertices on each side of the bipartite graph
        """
        if self.is_symetric:
            X = P[0]
            (nx, mx) = tuple(X.shape)
            if nx != mx:
                raise ValueError(f'Input preference scores should have same dimensions, got {nx} x {mx}')
            else:
                Y = np.transpose(X)
                return X, Y, nx
        else:
            X, Y = P[0], P[1]
            (nx, mx), (ny, my) = tuple(X.shape), tuple(Y.shape)
            if nx != mx or mx != ny or ny != my:
                raise ValueError(f'Input preference scores should have same dimensions, got {nx} x {mx} and {ny} x {my}')
            else:
                return X, Y, nx
    
    def solve(self, P):
        """
        Input:
            P: (numpy 2xnxn 3D array of floats) Uniform random set of preference scores
        Output:
            score: (float between 0 and 1) The ratio of pairs of couples in matching that are stable
            matching: (list of 2-tuples of ints) Matching computed to solve the problem instance
        """
        score, matching = 0.0, []
        return score, matching

if __name__ == '__main__':
    pass