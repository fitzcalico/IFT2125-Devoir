from setupQ2 import *

#######################################################################
### DÉBUT: vous pouvez ajouter des constantes/fonctions/classes ici ###
#######################################################################
default_B = 5 # Votre valeur de B préférée
default_R = 0.5 # Votre valeur de R préférée
default_theta = 0.5 # Votre valeur de theta préférée

#######################################################################
###  FIN : vous pouvez ajouter des constantes/fonctions/classes ici ###
#######################################################################

class GreedyFree(StructuredMatchingAlgorithm):

    def __init__(self, pretty_name='GreedyFree', R=None, B=None, theta=None):
        super().__init__(pretty_name, R, B, theta)
    
    ####################################################
    ### DÉBUT: vous pouvez ajouter des fonctions ici ###
    ####################################################
    
    ####################################################
    ###  FIN : vous pouvez ajouter des fonctions ici ###
    ####################################################
    def solve(self, X):
        """
        Input:
            X: (numpy nxm 2D array of floats) Uniform random set of preference scores
        Output:
            score: (float) Sum of preference scores of edges in matching
            matching: (list of 2-tuples of ints) Matching computed to solve the problem instance
        """
        (n, m) = tuple(X.shape)
        matching = []
        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################

        edges = []
        for i in range(n):
            for j in range(m):
                edges.append((X[i][j], i, j))
        edges.sort(reverse=True)

        used_i = set()
        used_j = set()

        for weight, i, j in edges:
            if weight <= 0: break
            if i in used_i or j in used_j: continue

            is_crossing = False
            for (a, b) in matching:
                if (a < i and b > j) or (a > i and b < j):
                    is_crossing = True
                    break

            if is_crossing: continue

            matching.append((i, j))
            used_i.add(i)
            used_j.add(j)

        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################
        # Les prochaines lignes en commentaires vous permettent de vérifier si votre algorithme respecte les contraintes.
        # À exécuter au choix.
        #if not isValidMatching(matching, X):
        #    print(matching)
        #    print(self.pretty_name)
        #    raise ValueError()
        score = 0.0
        for (i, j) in matching: score = round_decimals(score + X[i][j])
        return score, matching

class DynamicFree(StructuredMatchingAlgorithm):

    def __init__(self, pretty_name='DynamicFree', R=None, B=None, theta=None):
        super().__init__(pretty_name, R, B, theta)
    
    ####################################################
    ### DÉBUT: vous pouvez ajouter des fonctions ici ###
    ####################################################
    
    ####################################################
    ###  FIN : vous pouvez ajouter des fonctions ici ###
    ####################################################
    def solve(self, X):
        """
        Input:
            X: (numpy nxm 2D array of floats) Uniform random set of preference scores
        Output:
            score: (float) Sum of preference scores of edges in matching
            matching: (list of 2-tuples of ints) Matching computed to solve the problem instance
        """
        (n, m) = tuple(X.shape)
        matching = []
        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################

        T = [[0.0 for _ in range(m + 1)] for _ in range(n + 1)]
        choice = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                up = T[i - 1][j]
                left = T[i][j - 1]
                diag = T[i - 1][j - 1] + max(0, X[i - 1][j - 1])

                best = max(up, left, diag)
                T[i][j] = best

                if best == diag:
                    choice[i][j] = 2
                elif best == up:
                    choice[i][j] = 0
                else:
                    choice[i][j] = 1

        # backtracking
        i = n
        j = m

        while i > 0 and j > 0:
            if choice[i][j] == 2:
                if X[i - 1][j - 1] > 0:
                    matching.append((i - 1, j - 1))
                i -= 1
                j -= 1
            elif choice[i][j] == 0:
                i -= 1
            else:
                j -= 1

        matching.reverse()

        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################
        # Les prochaines lignes en commentaires vous permettent de vérifier si votre algorithme respecte les contraintes.
        # À exécuter au choix.
        if not isValidMatching(matching, X):
            print (matching)
            print(self.pretty_name)
            raise ValueError()
        score = 0.0
        for (i, j) in matching: score = round_decimals(score + X[i][j])
        return score, matching

class GreedyB(StructuredMatchingAlgorithm):

    def __init__(self, pretty_name='Greedy', R=None, B=default_B, theta=None):
        super().__init__(pretty_name, R, B, theta)
    
    ####################################################
    ### DÉBUT: vous pouvez ajouter des fonctions ici ###
    ####################################################
    
    ####################################################
    ###  FIN : vous pouvez ajouter des fonctions ici ###
    ####################################################
    def solve(self, X):
        """
        Input:
            X: (numpy nxm 2D array of floats) Uniform random set of preference scores
        Output:
            score: (float) Sum of preference scores of edges in matching
            matching: (list of 2-tuples of ints) Matching computed to solve the problem instance
        """
        (n, m) = tuple(X.shape)
        matching = []
        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################
        edges = []
        for i in range(n):
            for j in range(m):
                edges.append((X[i][j], i, j))
        edges.sort(reverse=True)

        used_i = set()
        used_j = set()

        for weight, i, j in edges:
            if weight <= 0: break
            if i in used_i or j in used_j: continue

            is_crossing = False
            for a, b in matching:
                if (a < i and b > j) or (a > i and b < j):
                    is_crossing = True
                    break
            if is_crossing: continue

            if matching:
                a, b = matching[-1]
                if abs(i - a) > self.B or abs(j - b) > self.B: continue

            matching.append((i, j))
            used_i.add(i)
            used_j.add(j)

        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################
        # Les prochaines lignes en commentaires vous permettent de vérifier si votre algorithme respecte les contraintes.
        # À exécuter au choix.
        # if not isValidMatching(matching, X, B=self.B):
        #     print(matching)
        #     print(self.pretty_name)
        #     raise ValueError()
        score = 0.0
        for (i, j) in matching: score = round_decimals(score + X[i][j])
        # print(score, self.B, n*m)
        return score, matching

class DynamicB(StructuredMatchingAlgorithm):

    def __init__(self, pretty_name='Dynamic', R=None, B=default_B, theta=None):
        super().__init__(pretty_name, R, B, theta)
    
    ####################################################
    ### DÉBUT: vous pouvez ajouter des fonctions ici ###
    ####################################################
    
    ####################################################
    ###  FIN : vous pouvez ajouter des fonctions ici ###
    ####################################################
    def solve(self, X):
        """
        Input:
            X: (numpy nxm 2D array of floats) Uniform random set of preference scores
        Output:
            score: (float) Sum of preference scores of edges in matching
            matching: (list of 2-tuples of ints) Matching computed to solve the problem instance
        """
        (n, m) = tuple(X.shape)
        matching = []
        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################

        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################
        # Les prochaines lignes en commentaires vous permettent de vérifier si votre algorithme respecte les contraintes.
        # À exécuter au choix.
        #if not isValidMatching(matching, X, B=self.B):
        #    print(matching)
        #    print(self.pretty_name)
        #    raise ValueError()
        score = 0.0
        for (i, j) in matching: score = round_decimals(score + X[i][j])
        return score, matching

class DynamicR(StructuredMatchingAlgorithm):

    def __init__(self, pretty_name='Dynamic', R=default_R, B=None, theta=None):
        super().__init__(pretty_name, R, B, theta)
    
    ####################################################
    ### DÉBUT: vous pouvez ajouter des fonctions ici ###
    ####################################################
    
    ####################################################
    ###  FIN : vous pouvez ajouter des fonctions ici ###
    ####################################################
    def solve(self, X):
        """
        Input:
            X: (numpy nxm 2D array of floats) Uniform random set of preference scores
        Output:
            score: (float) Sum of preference scores of edges in matching
            matching: (list of 2-tuples of ints) Matching computed to solve the problem instance
        """
        (n, m) = tuple(X.shape)             #      -100 < X[i][j] < 100
        K = round(self.R * min(n, m))
        P = probabilistic_transformation(X) #         0 < P[i][j] < 1
        Q = np.log(P)                       # -math.inf < Q[i][j] < 0
        matching = []
        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################
        
        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################
        # Les prochaines lignes en commentaires vous permettent de vérifier si votre algorithme respecte les contraintes.
        # À exécuter au choix.
        #if not isValidMatching(matching, X, K=K):
        #    print(matching)
        #    print(self.pretty_name)
        #    raise ValueError()
        score = 0.0
        for (i, j) in matching: score = round_decimals(score + X[i][j])
        return score, matching

class DynamicTheta(StructuredMatchingAlgorithm):

    def __init__(self, pretty_name='Dynamic', R=None, B=None, theta=default_theta):
        super().__init__(pretty_name, R, B, theta)
    
    ####################################################
    ### DÉBUT: vous pouvez ajouter des fonctions ici ###
    ####################################################
    
    ####################################################
    ###  FIN : vous pouvez ajouter des fonctions ici ###
    ####################################################
    def solve(self, X):
        """
        Input:
            X: (numpy nxm 2D array of floats) Uniform random set of preference scores
        Output:
            score: (float) Sum of preference scores of edges in matching
            matching: (list of 2-tuples of ints) Matching computed to solve the problem instance
        """
        (n, m) = tuple(X.shape)             #      -100 < X[i][j] < 100
        P = probabilistic_transformation(X) #         0 < P[i][j] < 1
        Q = np.log(P / self.theta)          # -math.inf < Q[i][j] < math.inf
        matching = []
        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################
        
        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################
        # Les prochaines lignes en commentaires vous permettent de vérifier si votre algorithme respecte les contraintes.
        # À exécuter au choix.
        #if not isValidMatching(matching, X, theta=self.theta):
        #    print(matching)
        #    print(self.pretty_name)
        #    raise ValueError()
        score = 0.0
        for (i, j) in matching: score = round_decimals(score + X[i][j])
        return score, matching

if __name__ == '__main__':
    import os
    for q in ['Question1', 'Question21', 'Question22', 'Question31',
              'Question32']:
        os.makedirs(f'figures/{q}', exist_ok=True)
    ################################################################################################
    ### Début: Modifiez le code ici pour faire des tests ou générer les figures que vous désirez ###
    ################################################################################################
    Tests = False
    Question1 = False
    Question21 = True
    Question22 = False
    Question31 = False
    Question32 = False
    if Tests:
        isOptimal(DynamicFree())
        isSubOptimal(GreedyFree())
    if Question1:
        identifier = f'Question1'
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        algorithms.append(GreedyFree())
        custom_sample_sizes.append(default_sample_sizes[:])
        algorithms.append(DynamicFree())
        custom_sample_sizes.append(default_sample_sizes[:])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    if Question21:
        identifier = f'Question21'
        yourBgrid = [1,5,8,13,21,50] # Les valeurs de B que vous voudriez tester
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        for B in yourBgrid:
            algorithms.append(GreedyB(B=B))
            custom_sample_sizes.append(default_sample_sizes[:])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    if Question22:
        identifier = f'Question22'
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        algorithms.append(GreedyFree())
        custom_sample_sizes.append(default_sample_sizes[:])
        algorithms.append(DynamicFree())
        custom_sample_sizes.append(default_sample_sizes[:])
        algorithms.append(GreedyB(B=default_B))
        custom_sample_sizes.append(default_sample_sizes[:])
        algorithms.append(DynamicB(B=default_B))
        custom_sample_sizes.append(default_sample_sizes[:])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    if Question31:
        identifier = f'Question31'
        yourRgrid = [0.5, 0.65, 0.8] # Les valeurs de R que vous voudriez tester
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid
        algorithms.append(DynamicFree())
        custom_sample_sizes.append([s // 5 for s in default_sample_sizes[:-3]])
        for R in yourRgrid:
            algorithms.append(DynamicR(R=R))
            custom_sample_sizes.append([s // 5 for s in default_sample_sizes[:-3]])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    if Question32:
        identifier = f'Question32'
        yourTgrid = [0.025, 0.25, 0.5, 0.75, 0.975] # Les valeurs de theta que vous voudriez tester
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid
        algorithms.append(DynamicFree())
        custom_sample_sizes.append([s // 2 for s in default_sample_sizes[:]])
        for theta in yourTgrid:
            algorithms.append(DynamicTheta(theta=theta))
            custom_sample_sizes.append([s // 2 for s in default_sample_sizes[:]])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    ################################################################################################
    ###  Fin : Modifiez le code ici pour faire des tests ou générer les figures que vous désirez ###
    ################################################################################################