print(f'Downloading modules...')
import time
import itertools
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import json
print(f'Downloading datasets...')
n_base = 10
default_sample_sizes = [160, 80, 40, 20, 10, 5]
default_n_grid = [n_base ** i for i in range(1, 1 + len(default_sample_sizes))]
dataset = dict()
with open('datasets/dataset1.json') as f: dataset[default_n_grid[0]] = json.load(f)
with open('datasets/dataset2.json') as f: dataset[default_n_grid[1]] = json.load(f)
with open('datasets/dataset3.json') as f: dataset[default_n_grid[2]] = json.load(f)
with open('datasets/dataset4.json') as f: dataset[default_n_grid[3]] = json.load(f)
with open('datasets/dataset5.json') as f: dataset[default_n_grid[4]] = json.load(f)
with open('datasets/dataset6.json') as f: dataset[default_n_grid[5]] = json.load(f)
for n_iter, n in enumerate(default_n_grid):
    for sample_iter in range(default_sample_sizes[n_iter]):
        dataset[n][sample_iter] = [tuple(p) for p in dataset[n][sample_iter]]
from datasets.solutions import solutions
print(f'Downloads successful!')
default_minimum, default_maximum = -100.0, 100.0
default_decimals = 4
default_d = 2
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

def generate_set_of_points(n, d=default_d, minima=None, maxima=None):
    """
    Input:
        n: (int) Number of points in the cloud
        d: (int) Dimensionality of the points (Here, d=2)
    Output:
        X: (list of d-tuples of floats) Uniform random set of points within {min,max}ima constraints
    """
    if minima and len(minima != default_d):
        raise ValueError(f'Expected minima to have d={default_d} values. Got {len(minima)} instead.')
    else:
        minima = [default_minimum for i in range(default_d)]
    if maxima and len(maxima != default_d):
        raise ValueError(f'Expected maxima to have d={default_d} values. Got {len(maxima)} instead.')
    else:
        maxima = [default_maximum for i in range(default_d)]
    X = [tuple(round_decimals(random.uniform(minima[j], maxima[j])) for j in range(default_d)) for i in range(n)]
    return X

def euclidean_distance_square(p, q):
    """
    Input:
        p: (tuple of floats) First of two points for which we want to compute the square of the euclidean distance
        q: (tuple of floats) Second point
    Output:
        square: (float) Square of the euclidean distance between p and q
    """
    square = sum((p[j] - q[j]) ** 2 for j in range(len(p)))
    return square

def euclidean_distance(p, q):
    """
    Input:
        p: (tuple of floats) First of two points for which we want to compute the euclidean distance
        q: (tuple of floats) Second point
    Output:
        distance: (float) Euclidean distance between p and q
    """
    square = euclidean_distance_square(p, q)
    distance = math.sqrt(square)
    return distance

def time_transformation(t):
    """
    Input:
        t: (float or np-array) Computation time(s) in microseconds
    Output:
        transformed_t: (float or np-array) Computation time(s) in log scale
    """
    return np.log10(1.0 + t)

def estimate_computation_time(algorithms, n_grid=default_n_grid, sample_sizes=None, verbose=True):
    """
    Input:
        algorithms: (list of Algorithm objects) Algorithms that compute two closest points
        n_grid: (list of ints) The numbers of points in the problem instances to generate
        sample_sizes: (list of list of ints) The numbers of times a problem instance of a certain size is generated, possibly different for each algorithm
    Output:
        computation_times_means: (list of list of floats) Means of log-scale computation times for each algo and problem size
        computation_times_stds: (list of list of floats) Standard deviations of log-scale computation times for each algo and problem size
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
    for n_iter, n in enumerate(n_grid):
        max_sample_size = max_sample_sizes[n_iter]
        if max_sample_size == 0: continue
        if verbose: print(f'Computing average computation times for n = {n}')
        for sample_iter in range(max_sample_size):
            if verbose and n_iter >= 3: print(f'\tRunning sample {sample_iter + 1}')
            if n in default_n_grid and sample_iter < default_sample_sizes[n_iter]: X = dataset[n][sample_iter]
            else: X = generate_set_of_points(n)
            for algo_iter, algorithm in enumerate(algorithms):
                if n_iter >= len(sample_sizes[algo_iter]): continue
                if sample_iter >= sample_sizes[algo_iter][n_iter]: continue
                start_time = time.perf_counter()
                p, q = algorithm.solve(X)
                computation_time = time.perf_counter() - start_time
                computation_times[algo_iter][n_iter].append(1e6 * computation_time)
    for algo_iter in range(len(algorithms)):
        for n_iter in range(len(sample_sizes[algo_iter])):
            time_array = time_transformation(np.array(computation_times[algo_iter][n_iter]))
            computation_times_means[algo_iter][n_iter] = np.mean(time_array)
            computation_times_stds[algo_iter][n_iter] = np.std(time_array)
    return computation_times_means, computation_times_stds

def plot_computation_times(algorithms, identifier, computation_times_means, computation_times_stds, n_grid):
    """
    Input:
        algorithms: (list of Algorithm objects) Algorithms that compute two closest points
        identifier: (string) Custom string for personalizing file names and paths
        computation_times_means: (list of lists of floats) Transformed mean computation times for each algorithm for each n in n_grid
        computation_times_stds: (list of lists of floats) Standard deviations corresponding to the means
        n_grid: (list of ints) The numbers of points in the problem instances that were generated
    Output:
        SAVED_FIGURE
    """
    log_n_grid = [math.log10(n) for n in n_grid]
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
    ax.set_xlabel(r'$\log_{10}(n)$', fontsize=12)
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

def compare_algorithms(algorithms, identifier, n_grid=default_n_grid, sample_sizes=default_sample_sizes, verbose=True):
    """
    Input:
        algorithms: (list of Algorithm objects) Algorithms that compute two closest points
        identifier: (string) Custom string for personalizing file names and paths
        n_grid: (list of ints) The sizes of the problem instances to generate/load
        sample_sizes: (list of list of ints) The numbers of times a problem instance of a certain size is generated/loaded;
                                             possibly different for each algorithm
    Output:
        SAVED_FIGURE
    """
    ct_means, ct_stds = estimate_computation_time(algorithms, n_grid, sample_sizes, verbose)
    plot_computation_times(algorithms, identifier, ct_means, ct_stds, n_grid)

def isOptimal(algorithm, n_grid=default_n_grid, sample_sizes=default_sample_sizes, verbose=True):
    """
    Input:
        algorithm: (DivideAndConquerAlgorithm object) Algorithm that compute optimal or suboptimal matching
        n_grid: (list of ints) The sizes of the problem instances to generate/load
        sample_sizes: (list of list of ints) The numbers of times a problem instance of a certain size is generated/loaded
    Output:
        isOptimal: (boolean) Indicates if the closest points computed by algorithm are indeed optimal
    """
    for n_iter, n in enumerate(n_grid):
        if n_iter >= len(sample_sizes): break
        if verbose: print(f'Verifying optimality for n = {n}')
        for sample_iter in range(sample_sizes[n_iter]):
            if n in default_n_grid and sample_iter < default_sample_sizes[n_iter]: X = dataset[n][sample_iter]
            else: continue
            if verbose and n_iter >= 4: print(f'\tRunning sample {sample_iter + 1}')
            solution = solutions[n][sample_iter]
            p, q = algorithm.solve(X)
            if (p, q) not in solution and (q, p) not in solution:
                print(algorithm.pretty_name + ' is not optimal.')
                print(f'Expected {solution}, but got {(p, q)}')
                return False
    print(algorithm.pretty_name + ' is optimal on all tested problems')
    return True

class NaiveAlgorithm():

    def __init__(self, pretty_name='Naive algorithm'):
        self.pretty_name = pretty_name

    def solve(self, X):
        """
        Input:
            X: (list of 2-tuples of floats) Uniform random set of points
        Output:
            (p, q): (2-tuple of 2-tuples of floats) The two closest points within X
        """
        min_distance = math.inf
        p, q = None, None
        for (candidate_p, candidate_q) in itertools.combinations(X, 2):
            distance = euclidean_distance_square(candidate_p, candidate_q)
            if distance < min_distance:
                p, q = candidate_p, candidate_q
                min_distance = distance
        return (p, q)

class DivideAndConquerAlgorithm:

    def __init__(self, pretty_name, corridor_k, base_size):
        self.corridor_k = corridor_k
        self.base_size = base_size
        self.pretty_name = f'{pretty_name}(k={corridor_k}, b={base_size})'
    
    def solve(self, X):
        """
        Input:
            X: (list of 2-tuples of floats) Uniform random set of points
        Output:
            (p, q): (2-tuple of 2-tuples of floats) The two closest points within X
        """
        return ((0.0, 0.0), (0.0, 0.0))

if __name__ == '__main__':
    pass