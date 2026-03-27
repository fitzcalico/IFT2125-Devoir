from setupQ1 import *

#######################################################################
### DÉBUT: vous pouvez ajouter des constantes/fonctions/classes ici ###
#######################################################################

#######################################################################
###  FIN : vous pouvez ajouter des constantes/fonctions/classes ici ###
#######################################################################

class SymmetricGreedy(StableMatchingAlgorithm):

    def __init__(self, pretty_name='SymmetricGreedy', symmetric=True):
        super().__init__(pretty_name, symmetric)
    
    ####################################################
    ### DÉBUT: vous pouvez ajouter des fonctions ici ###
    ####################################################
    
    ####################################################
    ###  FIN : vous pouvez ajouter des fonctions ici ###
    ####################################################
    def solve(self, P):
        """
        Input:
            P: (numpy 2xnxn 3D array of floats) Uniform random set of preference scores
        Output:
            score: (float between 0 and 1) The ratio of pairs of couples in matching that are stable
            matching: (list of 2-tuples of ints) Matching computed to solve the problem instance
        """
        X, Y, n = self.process_input(P) # Cas symétrique donc Y = np.transpose(X)
        score, matching = 0.0, []
        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################
        
        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################
        score = compute_matching_stability(matching, X, Y)
        return score, matching

class GaleShapleySorting(StableMatchingAlgorithm):

    def __init__(self, pretty_name='GSSorting', symmetric=False):
        super().__init__(pretty_name, symmetric)
    
    ####################################################
    ### DÉBUT: vous pouvez ajouter des fonctions ici ###
    ####################################################
    
    ####################################################
    ###  FIN : vous pouvez ajouter des fonctions ici ###
    ####################################################
    def solve(self, P):
        """
        Input:
            P: (numpy 2xnxn 3D array of floats) Uniform random set of preference scores
        Output:
            score: (float between 0 and 1) The ratio of pairs of couples in matching that are stable
            matching: (list of 2-tuples of ints) Matching computed to solve the problem instance
        """
        X, Y, n = self.process_input(P)
        score, matching = 0.0, []
        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################
        
        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################
        score = compute_matching_stability(matching, X, Y)
        return score, matching

class GaleShapleyMaximum(StableMatchingAlgorithm):

    def __init__(self, pretty_name='GSMaximum', symmetric=False):
        super().__init__(pretty_name, symmetric)
    
    ####################################################
    ### DÉBUT: vous pouvez ajouter des fonctions ici ###
    ####################################################
    
    ####################################################
    ###  FIN : vous pouvez ajouter des fonctions ici ###
    ####################################################
    def solve(self, P):
        """
        Input:
            P: (numpy 2xnxn 3D array of floats) Uniform random set of preference scores
        Output:
            score: (float between 0 and 1) The ratio of pairs of couples in matching that are stable
            matching: (list of 2-tuples of ints) Matching computed to solve the problem instance
        """
        X, Y, n = self.process_input(P)
        score, matching = 0.0, []
        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################
        
        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################
        score = compute_matching_stability(matching, X, Y)
        return score, matching

################################################################################
### Début: Vous pouvez implémenter autant de classes Greedy que vous désirez ###
################################################################################
class GreedyMaximum(StableMatchingAlgorithm):

    def __init__(self, pretty_name='GreedyMaximum', symmetric=False):
        super().__init__(pretty_name, symmetric)
    
    ####################################################
    ### DÉBUT: vous pouvez ajouter des fonctions ici ###
    ####################################################
    
    ####################################################
    ###  FIN : vous pouvez ajouter des fonctions ici ###
    ####################################################
    def solve(self, P):
        """
        Input:
            P: (numpy 2xnxn 3D array of floats) Uniform random set of preference scores
        Output:
            score: (float between 0 and 1) The ratio of pairs of couples in matching that are stable
            matching: (list of 2-tuples of ints) Matching computed to solve the problem instance
        """
        X, Y, n = self.process_input(P)
        score, matching = 0.0, []
        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################
        
        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################
        score = compute_matching_stability(matching, X, Y)
        return score, matching

class GreedyTrivial(StableMatchingAlgorithm):

    def __init__(self, pretty_name='GreedyTrivial', symmetric=False):
        super().__init__(pretty_name, symmetric)
    
    ####################################################
    ### DÉBUT: vous pouvez ajouter des fonctions ici ###
    ####################################################
    
    ####################################################
    ###  FIN : vous pouvez ajouter des fonctions ici ###
    ####################################################
    def solve(self, P):
        """
        Input:
            P: (numpy 2xnxn 3D array of floats) Uniform random set of preference scores
        Output:
            score: (float between 0 and 1) The ratio of pairs of couples in matching that are stable
            matching: (list of 2-tuples of ints) Matching computed to solve the problem instance
        """
        X, Y, n = self.process_input(P)
        score, matching = 0.0, []
        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################
        
        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################
        score = compute_matching_stability(matching, X, Y)
        return score, matching

################################################################################
###  Fin : Vous pouvez implémenter autant de classes Greedy que vous désirez ###
################################################################################

if __name__ == '__main__':
    #############################################################################
    ### Début: Modifiez le code ici pour générer les figures que vous désirez ###
    #############################################################################
    Tests = False
    Question1 = False
    Question2 = False
    Question3 = False
    
    if Tests:
        identifier = f'Tests'
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        algorithms.append(SymmetricGreedy())
        custom_sample_sizes.append(default_sample_sizes[:])
        algorithms.append(GaleShapleySorting())
        custom_sample_sizes.append(default_sample_sizes[:])
        algorithms.append(GaleShapleyMaximum())
        custom_sample_sizes.append(default_sample_sizes[:])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    if Question1:
        identifier = f'Question1'
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        algorithms.append(SymmetricGreedy())
        custom_sample_sizes.append(default_sample_sizes[:])
        algorithms.append(GaleShapleySorting(symmetric=True))
        custom_sample_sizes.append(default_sample_sizes[:])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    if Question2:
        identifier = f'Question2'
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        algorithms.append(SymmetricGreedy())
        custom_sample_sizes.append(default_sample_sizes[:])
        algorithms.append(GaleShapleySorting())
        custom_sample_sizes.append(default_sample_sizes[:])
        algorithms.append(GaleShapleyMaximum())
        custom_sample_sizes.append(default_sample_sizes[:])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    if Question3:
        identifier = f'Question3'
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        algorithms.append(GaleShapleySorting())
        custom_sample_sizes.append(default_sample_sizes[:])
        algorithms.append(GreedyMaximum())
        custom_sample_sizes.append(default_sample_sizes[:])
        algorithms.append(GreedyTrivial())
        custom_sample_sizes.append(default_sample_sizes[:])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    #############################################################################
    ###  Fin : Modifiez le code ici pour générer les figures que vous désirez ###
    #############################################################################