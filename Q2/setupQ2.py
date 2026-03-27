print(f'Downloading modules...')
import time
import itertools
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import json
print(f'Downloading datasets...')
default_sample_sizes = [160, 80, 40, 20, 10, 5]
default_n_grid = [2 ** (4 + i) for i in range(1, 1 + len(default_sample_sizes))]
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
from datasets.solutions import solutions
print(f'Downloads successful!')
default_minimum, default_maximum = -100.0, 100.0
default_decimals = 4
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

def probabilistic_transformation(X):
    """
    Input:
        X: (numpy nxn 2D array of floats) Uniform random set of preference scores
    Output:
        P: (numpy nxn 2D array of floats) Preference scores sent onto (0, 1) interval
    """
    return 1.0 / (1.0 + np.exp(-0.05 * X))

def generate_problem_instance(n, m, minimum=None, maximum=None):
    """
    Input:
        n: (int) Number of vertices on the left
        m: (int) Number of vertices on the right
    Output:
        X: (numpy nxn 2D array of floats) Uniform random set of preference scores
    """
    if minimum is None: minimum = default_minimum
    if maximum is None: maximum = default_maximum
    X = np.random.uniform(low=minimum, high=maximum, size=(n, m))
    return X

def time_transformation(t):
    """
    Input:
        t: (float or np-array) Computation time(s) in microseconds
    Output:
        transformed_t: (float or np-array) Computation time(s) in log scale
    """
    return np.log10(1.0 + t)

def isValidMatching(matching, X, B=None, K=None, theta=None):
    """
    Input:
        matching: (ordered list of 2-tuples of ints) Some matching
        X: (numpy nxn 2D array of floats) Uniform random set of preference scores
        B: (int) Maximum distance between two consecutive edges in matching
        K: (int) Exact required number of edges in matching
        theta: (float) Soft threshold over edge probability-score
    Output:
        isValidMatching: (boolean) Indicates if matching respects all constraints
    """
    (n, m) = tuple(X.shape)
    used_i, used_j = [False for i in range(n)], [False for j in range(m)]
    last_i, last_j = -1, -1
    orderred = True
    for (i, j) in matching:
        if used_i[i] or used_j[j]:
            print(f'Contrainte (i) non respectée')
            return False
        else: used_i[i] = True; used_j[j] = True
        if i <= last_i or j <= last_j: orderred = False
        last_i, last_j = i, j
    if not orderred:
        for ((i, j), (u, v)) in itertools.combinations(matching, 2):
            sense_i, sense_j = u - i, v - j
            if sense_i * sens_j < 0:
                print(f'Contrainte (ii) non respectée')
                return False
    if B is not None:
        if not orderred: matching = sorted(matching)
        for k in range(len(matching)-1):
            i, j = matching[k]
            u, v = matching[k+1]
            if u - i > B or v - j > B:
                print(f'Contrainte (iv) non respectée')
                return False
    if K is not None:
        if len(matching) != K:
            print(f'Contrainte (v) non respectée')
            return False
    if theta is not None:
        if not orderred: matching = sorted(matching)
        a, b = -1, -1
        for (i, j) in matching:
            if i - a > 1 and j - b > 1:
                print(f'Contrainte (iii) non respectée')
                return False
            a, b = i, j
    return True

def isOptimal(algorithm, n_grid=default_n_grid, sample_sizes=default_sample_sizes, epsilon=1e-3, verbose=True):
    """
    Input:
        algorithm: (StructuredMatchingAlgorithm object) Algorithm that compute optimal or suboptimal matching
        n_grid: (list of ints) The sizes of the problem instances to generate/load
        sample_sizes: (list of list of ints) The numbers of times a problem instance of a certain size is generated/loaded
        epsilon: (float) Numerical tolerance
    Output:
        isOptimal: (boolean) Indicates if computed scores are all contained within a +/- epsilon window of the optimal value
    """
    for n_iter, n in enumerate(n_grid):
        if n_iter >= len(sample_sizes): break
        if verbose: print(f'Verifying optimality for n = {n}')
        for sample_iter in range(sample_sizes[n_iter]):
            if n in default_n_grid and sample_iter < default_sample_sizes[n_iter]: X = dataset[n][sample_iter]
            else: continue
            if verbose and n_iter >= 3: print(f'\tRunning sample {sample_iter + 1}')
            score, matching = algorithm.solve(X)
            if abs(score - solutions[n][sample_iter]) > epsilon:
                print(algorithm.pretty_name.replace('$', '') + ' is not optimal')
                return False
    print(algorithm.pretty_name.replace('$', '') + ' is optimal')
    return True

def isSubOptimal(algorithm, n_grid=default_n_grid, sample_sizes=default_sample_sizes, epsilon=1e-3, verbose=True):
    """
    Input:
        algorithm: (StructuredMatchingAlgorithm object) Algorithm that compute optimal or suboptimal matching
        n_grid: (list of ints) The sizes of the problem instances to generate/load
        sample_sizes: (list of list of ints) The numbers of times a problem instance of a certain size is generated/loaded
        epsilon: (float) Numerical tolerance
    Output:
        isSubOptimal: (boolean) Indicates if computed scores are all below the optimal value + epsilon
    """
    for n_iter, n in enumerate(n_grid):
        if n_iter >= len(sample_sizes): break
        if verbose: print(f'Verifying suboptimality for n = {n}')
        for sample_iter in range(sample_sizes[n_iter]):
            if n in default_n_grid and sample_iter < default_sample_sizes[n_iter]: X = dataset[n][sample_iter]
            else: continue
            if verbose and n_iter >= 3: print(f'\tRunning sample {sample_iter + 1}')
            score, matching = algorithm.solve(X)
            if score > solutions[n][sample_iter] + epsilon:
                print(algorithm.pretty_name.replace('$', '') + ' is not suboptimal')
                return False
    print(algorithm.pretty_name.replace('$', '') + ' is suboptimal')
    return True

def estimate_computation_times(algorithms, n_grid=default_n_grid, sample_sizes=None, verbose=True):
    """
    Input:
        algorithms: (list of StructuredMatchingAlgorithm objects) Algorithms that compute optimal or suboptimal matching
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
            if n in default_n_grid and sample_iter < default_sample_sizes[n_iter]: X = dataset[n][sample_iter]
            else: X = generate_problem_instance(n, n)
            for algo_iter, algorithm in enumerate(algorithms):
                if n_iter >= len(sample_sizes[algo_iter]): continue
                if sample_iter >= sample_sizes[algo_iter][n_iter]: continue
                start_time = time.perf_counter()
                score, matching = algorithm.solve(X)
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
        algorithms: (list of StructuredMatchingAlgorithm objects) Algorithms that compute optimal or suboptimal matching
        identifier: (string) Custom string for personalizing file names and paths
        computation_times_means: (list of list of floats) Means of log-scale computation times for each algo and problem size
        computation_times_stds: (list of list of floats) Standard deviations of log-scale computation times for each algo and problem size
        n_grid: (list of ints) The sizes of the problem instances that were generated/loaded
    Output:
        SAVED_FIGURE
    """
    log_n_grid = [int(math.log2(n)) for n in n_grid]
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
    ax.set_xlabel(r'$\log_{2}(n)$', fontsize=12)
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
        algorithms: (list of StructuredMatchingAlgorithm objects) Algorithms that compute optimal or suboptimal matching
        identifier: (string) Custom string for personalizing file names and paths
        objective_values_means: (list of list of floats) Means of objective values for each algo and problem size
        objective_values_stds: (list of list of floats) Standard deviations of objective values for each algo and problem size
        n_grid: (list of ints) The sizes of the problem instances that were generated/loaded
    Output:
        SAVED_FIGURE
    """
    log_n_grid = [int(math.log2(n)) for n in n_grid]
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
    ax.set_title(f'Influence of problem size ' + r'$n$' + ' over objective value', fontsize=14, pad=15)
    ax.set_xlabel(r'$\log_{2}(n)$', fontsize=12)
    ax.set_ylabel(f'Objective value', fontsize=12)
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
        algorithms: (list of StructuredMatchingAlgorithm objects) Algorithms that compute optimal or suboptimal matching
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

class StructuredMatchingAlgorithm:

    def __init__(self, pretty_name, R=None, B=None, theta=None):
        if B is not None:
            if type(B) != type(1) or B < 1:
                raise ValueError(f'Parameter B should be a non-negative integer, got {B}')
        self.B = B
        if R is not None:
            if type(R) != type(1.0) or R < 0.0 or R > 1.0:
                raise ValueError(f'Parameter R should be a floating number between 0.0 and 1.0, got {R}')
            else:
                self.R = round_decimals(R)
        else:
            self.R = R
        if theta is not None:
            if type(theta) != type(1.0) or theta < 0.0 or theta > 1.0:
                raise ValueError(f'Parameter theta should be a floating number between 0.0 and 1.0, got {theta}')
            else:
                self.theta = round_decimals(theta)
        else:
            self.theta = theta
        self.pretty_name = f'{pretty_name}('
        if R is not None:
            self.pretty_name += r'$R =$' + str(R)
            if B is not None:
                self.pretty_name += r'$, B =$' + str(B)
            if theta is not None:
                self.pretty_name += r'$, \theta =$' + str(theta)
        elif B is not None:
            self.pretty_name += r'$B =$' + str(B)
            if theta is not None:
                self.pretty_name += r'$, \theta =$' + str(theta)
        elif theta is not None:
            self.pretty_name += r'$\theta =$' + str(theta)
        self.pretty_name += r'$)$'
    
    def solve(self, X):
        """
        Input:
            X: (numpy nxn 2D array of floats) Uniform random set of preference scores
        Output:
            score: (float) Sum of (possibly transformed) preference scores of edges in matching
            matching: (list of 2-tuples of ints) Matching computed to solve the problem instance
        """
        score, matching = 0.0, []
        return score, matching

if __name__ == '__main__':
    pass