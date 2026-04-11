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
        pairs = []

        # créer toutes les paires possibles
        for i in range(n):
            for j in range(n):
                pairs.append((X[i][j], i, j))

        pairs.sort(reverse=True)

        used_men = []
        used_women = []

        for w,i,j in pairs:
            if (i not in used_men) and (j not in used_women):
                matching.append((i, j))
                used_men.append(i)
                used_women.append(j)

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
            P: (numpy 2xNxN 3D array of floats) Uniform random set of preference scores
        Output:
            score: (float between 0 and 1) The ratio of pairs of couples in matching that are stable
            matching: (list of 2-tuples of ints) Matching computed to solve the problem instance
        """
        X, Y, n = self.process_input(P)
        score, matching = 0.0, []

        ##############################################
        ### Début: Fonction héritée, à implémenter ###
        ##############################################
        # trier lignes de X (retourne liste d'indices)
        men_preferences = []
        for m in range(n):
            sorted_women = np.argsort(-X[m])
            men_preferences.append(list(sorted_women))

        # table des "rangs" des femmes
        women_rank = []
        for w in range(n):
            sorted_men = np.argsort(-Y[w])
            rank = [0] * n
            for position, m in enumerate(sorted_men):
                rank[m] = position
            women_rank.append(rank)

        free_men = list(range(n))  # hommes restants
        next_proposal = [0] * n
        woman_partner = [-1] * n

        while free_men:
            m = free_men.pop(0)  # prendre premier homme des restants
            w = men_preferences[m][next_proposal[m]]  # prendre femme préférée de l'homme
            next_proposal[m] += 1

            if woman_partner[w] == -1: # si w célibataire
                woman_partner[w] = m   # former couple
            else:
                current = woman_partner[w]
                if women_rank[w][m] < women_rank[w][current]: # si w préfère m à m'
                    woman_partner[w] = m     # (m, w) forme couple
                    free_men.append(current) # m' devient célibataire
                else:
                    free_men.append(m)       # sinon (m', w) reste couple

        matching = [(m, w) for w, m in enumerate(woman_partner) if m != -1]

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

        # table des "rangs" des femmes
        women_rank = []
        for w in range(n):
            sorted_men = np.argsort(-Y[w])
            rank = [0] * n
            for position, m in enumerate(sorted_men):
                rank[m] = position
            women_rank.append(rank)

        free_men = list(range(n))  # hommes restants
        proposed = [[False] * n for _ in range(n)]
        woman_partner = [-1] * n

        while free_men:
            m = free_men.pop(0)  # prendre premier homme des restants

            # trouver meilleure femme célibataire
            w = -1
            best_score = -float("inf")
            for j in range(n):
                if not proposed[m][j] and X[m][j] > best_score:
                    best_score = X[m][j]
                    w = j
            proposed[m][w] = True

            if woman_partner[w] == -1: # si w célibataire
                woman_partner[w] = m   # former couple
            else:
                current = woman_partner[w]
                if women_rank[w][m] < women_rank[w][current]: # si w préfère m à m'
                    woman_partner[w] = m     # (m, w) forme couple
                    free_men.append(current) # m' devient célibataire
                else:
                    free_men.append(m)       # sinon (m', w) reste couple

        matching = [(m, w) for w, m in enumerate(woman_partner) if m != -1]


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
        # trier lignes de X (retourne liste d'indices)
        men_preferences = []
        for m in range(n):
            sorted_women = np.argsort(-X[m])
            men_preferences.append(list(sorted_women))

        free_men = list(range(n))  # hommes restants
        next_proposal = [0] * n
        woman_partner = [-1] * n

        while free_men:
            m = free_men.pop(0)    # prendre premier homme des restants
            w = men_preferences[m][next_proposal[m]] # prendre femme préférée de l'homme
            next_proposal[m] += 1

            if woman_partner[w] == -1:
                matching.append((m, w))

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
        matching = [(i, i) for i in range(n)]  # génère {(1,1), (2,2), ..., (n,n)}

        if len(matching) == 0:
            return 0.0, [0]
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
    Question1 = True
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
        algorithms.append(GaleShapleyMaximum(symmetric=True))
        custom_sample_sizes.append(default_sample_sizes[:])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    if Question2:
        identifier = f'Question2'
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        # algorithms.append(SymmetricGreedy())
        # custom_sample_sizes.append(default_sample_sizes[:])
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
