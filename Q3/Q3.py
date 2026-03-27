from setupQ3 import *

#######################################################################
### DÉBUT: vous pouvez ajouter des constantes/fonctions/classes ici ###
#######################################################################
default_corridor_k = 7 # Mettez votre réponse à la question 0.5 ici
base_size_q1 = 3       # Mettez votre valeur de b préférée suite à la question 1 (SortThenDivide)
base_size_q2 = 3       # Mettez votre valeur de b préférée suite à la question 2 (DivideThenSort)
base_size_q3 = 3       # Mettez votre valeur de b préférée suite à la question 3 (SortThenDivideAlternate)

#######################################################################
###  FIN : vous pouvez ajouter des constantes/fonctions/classes ici ###
#######################################################################

class SortThenDivide(DivideAndConquerAlgorithm):

    def __init__(self, pretty_name='SortThenDivide', corridor_k=default_corridor_k, base_size=base_size_q1):
        super().__init__(pretty_name, corridor_k, base_size)
    
    ####################################################
    ### DÉBUT: vous pouvez ajouter des fonctions ici ###
    ####################################################
    
    ####################################################
    ###  FIN : vous pouvez ajouter des fonctions ici ###
    ####################################################
    def solve(self, X):
        """
        Input:
            X: (list of 2-tuples of floats) Uniform random set of points
        Output:
            (p, q): (2-tuple of 2-tuples of floats) The two closest points within X
        """
        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################
        return ((0.0, 0.0), (0.0, 0.0))
        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################

class DivideThenSort(DivideAndConquerAlgorithm):

    def __init__(self, pretty_name='DivideThenSort', corridor_k=default_corridor_k, base_size=base_size_q2):
        super().__init__(pretty_name, corridor_k, base_size)
    
    ####################################################
    ### DÉBUT: vous pouvez ajouter des fonctions ici ###
    ####################################################
    
    ####################################################
    ###  FIN : vous pouvez ajouter des fonctions ici ###
    ####################################################
    def solve(self, X):
        """
        Input:
            X: (list of 2-tuples of floats) Uniform random set of points
        Output:
            (p, q): (2-tuple of 2-tuples of floats) The two closest points within X
        """
        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################
        return ((0.0, 0.0), (0.0, 0.0))
        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################

class SortThenDivideAlternate(DivideAndConquerAlgorithm):

    def __init__(self, pretty_name='SortThenDivideAlternate', corridor_k=default_corridor_k, base_size=base_size_q3):
        super().__init__(pretty_name, corridor_k, base_size)
    
    ####################################################
    ### DÉBUT: vous pouvez ajouter des fonctions ici ###
    ####################################################
    
    ####################################################
    ###  FIN : vous pouvez ajouter des fonctions ici ###
    ####################################################
    def solve(self, X):
        """
        Input:
            X: (list of 2-tuples of floats) Uniform random set of points
        Output:
            (p, q): (2-tuple of 2-tuples of floats) The two closest points within X
        """
        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################
        return ((0.0, 0.0), (0.0, 0.0))
        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################

if __name__ == '__main__':
    ######################################################################################
    ### Début: Modifiez le code ici pour générer les figures et répondre aux questions ###
    ######################################################################################
    Tests = False
    Question1 = False
    Question2 = False
    Question3 = False
    Question4 = False
    Question5 = False
    if Tests:
        isOptimal(SortThenDivide(), n_grid=default_n_grid[:-1])
        isOptimal(DivideThenSort(), n_grid=default_n_grid[:-1])
        isOptimal(SortThenDivideAlternate(), n_grid=default_n_grid[:-1])
    if Question1:
        identifier = f'Question1'
        yourBaseSizegrid = [3, 6, 12, 24, 48] # Les valeurs de base_size que vous voudriez tester
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        for base_size in yourBaseSizegrid:
            algorithms.append(SortThenDivide(base_size=base_size))
            custom_sample_sizes.append([s // 2 for s in default_sample_sizes[:-1]])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    if Question2:
        identifier = f'Question2'
        yourBaseSizegrid = [3, 6, 12, 24, 48] # Les valeurs de base_size que vous voudriez tester
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        for base_size in yourBaseSizegrid:
            algorithms.append(DivideThenSort(base_size=base_size))
            custom_sample_sizes.append([s // 2 for s in default_sample_sizes[:-1]])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    if Question3:
        identifier = f'Question3'
        yourBaseSizegrid = [3, 6, 12, 24, 48] # Les valeurs de base_size que vous voudriez tester
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        for base_size in yourBaseSizegrid:
            algorithms.append(SortThenDivideAlternate(base_size=base_size))
            custom_sample_sizes.append([s // 2 for s in default_sample_sizes[:-1]])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    if Question4:
        identifier = f'Question4'
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        algorithms.append(NaiveAlgorithm())
        custom_sample_sizes.append([s // 2 for s in default_sample_sizes[:-2]])
        algorithms.append(SortThenDivide())
        custom_sample_sizes.append([s // 2 for s in default_sample_sizes[:]])
        algorithms.append(DivideThenSort())
        custom_sample_sizes.append([s // 2 for s in default_sample_sizes[:]])
        algorithms.append(SortThenDivideAlternate())
        custom_sample_sizes.append([s // 2 for s in default_sample_sizes[:]])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    if Question5:
        verifying_optimality = True
        identifier = f'Question5'
        yourCorridorKgrid = [1, 4, 7] # Les valeurs de corridor_k que vous voudriez tester
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        for corridor_k in yourCorridorKgrid:
            algorithm = SortThenDivideAlternate(corridor_k=corridor_k)
            algorithms.append(algorithm)
            if verifying_optimality: isOptimal(algorithm, n_grid=default_n_grid[:-1])
            custom_sample_sizes.append([s // 2 for s in default_sample_sizes[:-1]])
        if not verifying_optimality: compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    ######################################################################################
    ###  Fin : Modifiez le code ici pour générer les figures et répondre aux questions ###
    ######################################################################################