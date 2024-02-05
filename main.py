import random


class EvolutionaryAlgorithm:
    """
    A class representing an evolutionary algorithm.

    Attributes:
    - population_size (int): The size of the population.
    - mutation_rate (float): The rate of mutation.
    - crossover_rate (float): The rate of crossover.

    Methods:
    - initialize_population(): Initializes the population with random individuals.
    - evaluate_fitness(): Evaluates the fitness of each individual in the population.
    - selection(): Performs selection to choose parents for reproduction.
    - crossover(): Performs crossover to create offspring.
    - mutation(): Performs mutation on the offspring.
    - replace_population(): Replaces the current population with the offspring.
    - run(): Runs the evolutionary algorithm.
    """

    def __init__(
        self,
        population_size: int = 30,
        no_of_offsprings: int = 10,
        no_of_generations: int = 50,
        mutation_rate: float = 0.5,
        no_of_iterations: int = 10,
    ) -> None:
        self.population_size = population_size
        self.no_of_offsprings = no_of_offsprings
        self.no_of_generations = no_of_generations
        self.mutation_rate = mutation_rate
        self.no_of_iterations = no_of_iterations
        self.parent_selection_scheme = 1
        self.survivor_selection_scheme = 1
        self.offsprings = []

    def initialize_population(self) -> None:
        # Initialize the population with random individuals
        self.population = {i: self.chromosome() for i in range(self.population_size)}
        return self.population

    def parent_selection(self) -> None:
        """
        Performs selection to choose parents for reproduction.
        """
        if self.parent_selection_scheme == 1:
            self.parents = self.fitness_proportionate_selection(self.no_of_offsprings)
        elif self.parent_selection_scheme == 2:
            self.parents = self.rank_based_selection(self.no_of_offsprings)
        elif self.parent_selection_scheme == 3:
            self.parents = self.binary_tournament_selection(self.no_of_offsprings)
        elif self.parent_selection_scheme == 4:
            self.parents = self.truncation_selection(self.no_of_offsprings)
        elif self.parent_selection_scheme == 5:
            self.parents = self.random_selection(self.no_of_offsprings)
        else:
            print("Invalid selection scheme")

    def crossover(self) -> None:
        # helper
        self.offsprings = []
        def fillRest(arr, offspring) -> None:
            remaining_cities = []
            for i in range(end, length + start + end):
                index = i % length
                remaining = arr[index]
                # print(arr2[index], i, index)
                if remaining not in offspring:
                    remaining_cities.append(remaining)
            remaining_cities.reverse()

            for i in range(end, length + start):
                index = i % length
                offspring[index % length] = remaining_cities.pop()

        # Perform crossover to create offspring
        for index in range(0, len(self.parents), 2):
            chromosome_parent1 = self.population[self.parents[index]]
            chromosome_parent2 = self.population[self.parents[index + 1]]

            length = len(chromosome_parent1)
            start, end = sorted(random.sample(range(length), 2))
            offspring1 = [None] * length
            offspring2 = [None] * length

            offspring1[start:end] = chromosome_parent1[start:end]
            offspring2[start:end] = chromosome_parent2[start:end]

            fillRest(chromosome_parent2, offspring1)
            fillRest(chromosome_parent1, offspring2)

            self.offsprings.append(offspring1)
            self.offsprings.append(offspring2)

    def mutation(self) -> None:
        for i in range(len(self.offsprings)):
            index1 = random.randint(0,len(self.offsprings[i]) - 1)
            index2 = random.randint(0,len(self.offsprings[i]) - 1)
            self.offsprings[i][index1], self.offsprings[i][index2] = self.offsprings[i][index2], self.offsprings[i][index1]

    def survivor_selection(self) -> None:
        """
        Performs selection to choose parents for reproduction.
        """
        if self.survivor_selection_scheme == 1:
            self.population = self.fitness_proportionate_selection(self.population)
        elif self.survivor_selection_scheme == 2:
            self.population = self.rank_based_selection(self.population)
        elif self.survivor_selection_scheme == 3:
            self.population = self.binary_tournament_selection(self.population)
        elif self.survivor_selection_scheme == 4:
            self.population = self.truncation_selection(self.population)
        elif self.survivor_selection_scheme == 5:
            self.population = self.random_selection(self.population)
        else:
            print("Invalid selection scheme")

    def run(self):
        # Run the evolutionary algorithm
        self.initialize_population()
        pass

    # Selection schemes
    def fitness_proportionate_selection(self, selection_size) -> list:
        total_fitness = sum(self.fitness_dictionary.values())
        probabilities = [
            fitness / total_fitness for fitness in self.fitness_dictionary.values()
        ]
        return random.choices(
            list(self.fitness_dictionary.keys()),
            weights=probabilities,
            k=selection_size,
        )

    def rank_based_selection(self, selection_size) -> list:
        temp_sorted = dict(
            sorted(
                self.fitness_dictionary.items(), key=lambda item: item[1], reverse=True
            )
        )
        ranks = [i for i in range(1, len(temp_sorted) + 1)]
        probabilities = [rank / sum(ranks) for rank in ranks]
        return random.choices(
            list(temp_sorted.keys()), weights=probabilities, k=selection_size
        )

    def binary_tournament_selection(self, selection_size) -> list:
        tournament_selected = []
        for i in range(selection_size):
            parent1, parent2 = random.choices(list(self.fitness_dictionary.keys()), k=2)
            if self.fitness_dictionary[parent1] > self.fitness_dictionary[parent2]:
                tournament_selected.append(parent1)
            else:
                tournament_selected.append(parent2)
        return tournament_selected

    def truncation_selection(self, selection_size) -> list:
        trunc = dict(sorted(self.fitness_dictionary.items(), key=lambda item: item[1]))
        return list(trunc.keys())[:selection_size]

    def random_selection(self, selection_size) -> list:
        return random.choices(list(self.fitness_dictionary.keys()), k=selection_size)
