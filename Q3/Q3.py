from setupQ3 import *

#######################################################################
### DÉBUT: vous pouvez ajouter des constantes/fonctions/classes ici ###
#######################################################################
default_corridor_k = 5  # Mettez votre réponse à la question 0.5 ici
base_size_q1 = 20  # Mettez votre valeur de b préférée suite à la question 1 (SortThenDivide)
base_size_q2 = 20  # Mettez votre valeur de b préférée suite à la question 2 (DivideThenSort)
base_size_q3 = 3  # Mettez votre valeur de b préférée suite à la question 3 (SortThenDivideAlternate)
#######################################################################
###  FIN : vous pouvez ajouter des constantes/fonctions/classes ici ###
#######################################################################

class SortThenDivide(DivideAndConquerAlgorithm):

    def __init__(self, pretty_name='SortThenDivide',
                 corridor_k=default_corridor_k, base_size=base_size_q1):
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

        Px = sorted(X, key=lambda p: p[0])  # trie par x dimension 1
        Py = sorted(X, key=lambda p: p[1])  # trie par y trie une seule fois pour

        # eviter de le refaire a chaque niveau et
        # ainsi garde la complexite en O(n log n)

        # fonction recursive
        def closest_pair_rec(Px, Py):
            n = len(Px)
            # le cas de base
            if n <= self.base_size:
                min_dist = float('inf')  # si le nmb de points est petit alors on fait une recherche naive O(n^2)
                p_closest, q_closest = None, None
                for i in range(n):
                    for j in range(i + 1, n):
                        dist = euclidean_distance_square(Px[i], Px[j])

                        if dist < min_dist:
                            min_dist = dist
                            p_closest, q_closest = Px[i], Px[j]
                return p_closest, q_closest, min_dist

            # on coupe ici la liste en deux selon laxe x et on résout chacune des moitiés récursivement
            # et on obtient les deux meilleurs couples et leurs distances
            mid = n // 2
            mid_x = Px[mid][0]
            Px_left = Px[:mid]
            Px_right = Px[mid:]

            Py_left = [p for p in Py if p[0] <= mid_x]
            Py_right = [p for p in Py if p[0] > mid_x]

            p_1, q_1, d_1 = closest_pair_rec(Px_left, Py_left)
            p_r, q_r, d_r = closest_pair_rec(Px_right, Py_right)

            if d_1 < d_r:
                p_best, q_best, delta = p_1, q_1, d_1
            else:
                p_best, q_best, delta = p_r, q_r, d_r

            strip = [p for p in Py if abs(p[0] - mid_x) < math.sqrt(delta)]

            for i in range(len(strip)):
                for j in range(i + 1, min(i + self.corridor_k + 1, len(strip))):
                    d = euclidean_distance_square(strip[i], strip[j])
                    if d < delta:
                        delta = d
                        p_best, q_best = strip[i], strip[j]

            return p_best, q_best, delta

        # Appel récursif
        p, q, _ = closest_pair_rec(Px, Py)
        return (p, q)

        ##############################################
        ###  Fin : Fonction héritée, à implémenter ###
        ##############################################


class DivideThenSort(DivideAndConquerAlgorithm):

    def __init__(self, pretty_name='DivideThenSort',
                 corridor_k=default_corridor_k, base_size=base_size_q2):
        super().__init__(pretty_name, corridor_k, base_size)

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

        # copie triée de tous les points selon la coordonnée x et pas selon y
        X_sorted_x = sorted(X, key=lambda p: p[0])

        def closest_pair_rec(pts):  # prend toujours une liste triée par x
            n = len(pts)

            # Cas de base recherche naïve
            if n <= self.base_size:
                min_dist = float('inf')
                p_best, q_best = pts[0], pts[1]
                for i in range(n):
                    for j in range(i + 1, n):
                        d = euclidean_distance_square(pts[i], pts[j])
                        if d < min_dist:
                            min_dist = d
                            p_best, q_best = pts[i], pts[j]
                return p_best, q_best, min_dist

            # Division avec mid et mid_x appels récursifs gauche/droite
            mid = n // 2
            mid_x = pts[mid][0]
            # appel récursif
            p_l, q_l, d_l = closest_pair_rec(pts[:mid])
            p_r, q_r, d_r = closest_pair_rec(pts[mid:])

            if d_l < d_r:
                best_p, best_q, best_d = p_l, q_l, d_l
            else:
                best_p, best_q, best_d = p_r, q_r, d_r

            # Corridor on filtre les points dans la bande
            strip = [p for p in pts if abs(p[0] - mid_x) ** 2 < best_d]

            # puis à chaque fusion on trie les points du corridor selon y
            strip.sort(key=lambda p: p[1])

            # Comparer les k voisins dans la bande
            for i in range(len(strip)):
                for j in range(i + 1,
                               min(i + self.corridor_k + 1, len(strip))):
                    d = euclidean_distance_square(strip[i], strip[j])
                    if d < best_d:
                        best_d = d
                        best_p, best_q = strip[i], strip[j]

                return best_p, best_q, best_d

        p, q, _ = closest_pair_rec(X_sorted_x)
        return (p, q)


class SortThenDivideAlternate(DivideAndConquerAlgorithm):

    def __init__(self, pretty_name='SortThenDivideAlternate',
                 corridor_k=default_corridor_k, base_size=base_size_q3):
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
    Question1 = True
    Question2 = True
    Question3 = False
    Question4 = False
    Question5 = False
    if Tests:
        isOptimal(SortThenDivide(), n_grid=default_n_grid[:-1])
        isOptimal(DivideThenSort(), n_grid=default_n_grid[:-1])
        isOptimal(SortThenDivideAlternate(), n_grid=default_n_grid[:-1])
    if Question1:
        identifier = f'Question1'
        yourBaseSizegrid = [3, 5, 10, 20, 35, 45, 60, 100, 150, 200]  # Les valeurs de base_size que vous voudriez tester
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        for base_size in yourBaseSizegrid:
            algorithms.append(SortThenDivide(base_size=base_size))
            custom_sample_sizes.append(
                [s // 2 for s in default_sample_sizes[:-1]])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    if Question2:
        identifier = f'Question2'
        yourBaseSizegrid = [3, 5, 10, 20, 35, 45, 60, 100, 150, 200]  # Les valeurs de base_size que vous voudriez tester
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        for base_size in yourBaseSizegrid:
            algorithms.append(DivideThenSort(base_size=base_size))
            custom_sample_sizes.append(
                [s // 2 for s in default_sample_sizes[:-1]])
        compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    if Question3:
        identifier = f'Question3'
        yourBaseSizegrid = [3, 6, 12, 24, 48]  # Les valeurs de base_size que vous voudriez tester
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
        yourCorridorKgrid = [1, 4, 7]  # Les valeurs de corridor_k que vous voudriez tester
        algorithms, custom_sample_sizes, custom_n_grid = [], [], default_n_grid[:]
        for corridor_k in yourCorridorKgrid:
            algorithm = SortThenDivideAlternate(corridor_k=corridor_k)
            algorithms.append(algorithm)
            if verifying_optimality: isOptimal(algorithm, n_grid=default_n_grid[:-1])
            custom_sample_sizes.append(
                [s // 2 for s in default_sample_sizes[:-1]])
        if not verifying_optimality: compare_algorithms(algorithms, identifier, n_grid=custom_n_grid, sample_sizes=custom_sample_sizes)
    ######################################################################################
    ###  Fin : Modifiez le code ici pour générer les figures et répondre aux questions ###
    ######################################################################################