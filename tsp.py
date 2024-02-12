import random

from main import EvolutionaryAlgorithm


class TSP(EvolutionaryAlgorithm):

    def __init__(
        self,
        filename,
        parent_selection_scheme,
        survival_selection_scheme,
        population_size,
        no_of_generations,
        no_of_offsprings,
        mutation_rate,
        no_of_iterations,
    ):
        super().__init__(
            parent_selection_scheme,
            survival_selection_scheme,
            population_size,
            no_of_generations,
            no_of_offsprings,
            mutation_rate,
            no_of_iterations,
        )
        self.parent_selection_scheme = parent_selection_scheme
        self.survival_selection_scheme = survival_selection_scheme
        self.no_of_offsprings = no_of_offsprings
        self.population_size = population_size
        self.no_of_generations = no_of_generations
        self.no_of_offsprings = no_of_offsprings
        self.mutation_rate = mutation_rate
        self.no_of_iterations = no_of_iterations

        self.filename = filename
        self.comment1 = ""
        self.comment2 = ""
        self.type = ""
        self.dimension = 0
        self.edgeWeightType = ""
        self.nodeCoordSelection = ""
        self.node_coords = []
        self.distance_matrix = []
        self.read_file()

    def read_file(self):
        with open(self.filename, "r") as f:
            self.name = f.readline().strip()
            self.comment1 = f.readline().strip()
            self.comment2 = f.readline().strip()
            self.type = f.readline().strip()
            self.dimension = int(f.readline().strip().split()[2])
            self.edgeWeightType = f.readline().strip()
            self.nodeCoordSelection = f.readline().strip()

            line = f.readline().strip()
            while line != "EOF":
                self.node_coords.append(list(map(float, line.split())))
                line = f.readline().strip()

        self.distance_matrix = [
            [0 for _ in range(self.dimension)] for _ in range(self.dimension)
        ]
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.distance_matrix[i][j] = self.euclidean_distance(
                    self.node_coords[i], self.node_coords[j]
                )

    def euclidean_distance(self, p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def chromosome(self) -> list:
        arr = [i for i in range(self.dimension)]
        random.shuffle(arr)
        return arr

    def evaluate_fitness(self, chromosome) -> float:
        fitness = 0
        for i in range(self.dimension - 1):
            fitness += self.distance_matrix[chromosome[i]][chromosome[i + 1]]
        fitness += self.distance_matrix[chromosome[self.dimension - 1]][chromosome[0]]
        return fitness

    def compute_population_fitness(self, population: dict) -> dict:
        fitness_dictionary = {}
        for individual, chromosome in population.items():
            fitness_dictionary[individual] = self.evaluate_fitness(chromosome)
        return fitness_dictionary


filename = "qa194.tsp"
population_size = 30
no_of_offsprings = 10
no_of_generations = 22000
mutation_rate = 0.5
no_of_iterations = 10
parent_selection = 1
survival_selection = 4

tsp = TSP(
    filename=filename,
    parent_selection_scheme=parent_selection,
    survival_selection_scheme=survival_selection,
    population_size=population_size,
    no_of_generations=no_of_generations,
    no_of_offsprings=no_of_offsprings,
    mutation_rate=mutation_rate,
    no_of_iterations=no_of_iterations,
)
tsp.run()


# print(data[parent1])
# print(fitness[parent1])
# print(data[parent2])
# print(fitness[parent2])


# print(tsp.crossover())


# arr1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# arr2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]

# length = len(arr1)
# start, end = sorted(random.sample(range(length), 2))
# offspring = [None] * length

# print("arr1", arr1)
# print("arr2", arr2)
# offspring[start:end] = arr1[start:end]

# check = end
# remaining_cities = []

# for i in range(end, length + start + end):
#     index = i % length
#     arr2Remaining = arr2[index]
#     # print(arr2[index], i, index)
#     if arr2Remaining not in offspring:
#         remaining_cities.append(arr2Remaining)
# remaining_cities.reverse()


# for i in range(end, length + start):
#     index = i % length
#     offspring[index % length] = remaining_cities.pop()

# print(offspring)
