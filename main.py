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

        self.selection_scheme = 1

    def initialize_population(self) -> None:
        # Initialize the population with random individuals
        self.population = {i: self.chromosome() for i in range(self.population_size)}

    def selection(self) -> None:
        """
        Performs selection to choose parents for reproduction.
        """
        if self.selection_scheme == 1:
            self.parents = self.fitness_proportionate_selection()
        elif self.selection_scheme == 2:
            self.parents = self.rank_based_selection()
        elif self.selection_scheme == 3:
            self.parents = self.binary_tournament_selection()
        elif self.selection_scheme == 4:
            self.parents = self.truncation_selection()
        elif self.selection_scheme == 5:
            self.parents = self.random_selection()
        else:
            print("Invalid selection scheme")

    def crossover(self):
        # Perform crossover to create offspring
        parent1, parent2 = self.parents

        chromosome_parent1 = self.population[parent1]
        chromosome_parent2 = self.population[parent2]

        length = len(chromosome_parent1)
        start, end = sorted(random.sample(range(length), 2))

        offspring = chromosome_parent1[start:end]
        remaining_cities = [
            city for city in chromosome_parent2 if city not in offspring
        ]
        offspring.extend(remaining_cities)

        return offspring

    def mutation(self):
        # Perform mutation on the offspring
        pass

    def replace_population(self):
        # Replace the current population with the offspring
        pass

    def run(self):
        # Run the evolutionary algorithm
        self.initialize_population()

        # stoppping condition
        # while not stopping_condition:
        # self.evaluate_fitness()
        # self.selection()
        # self.crossover()
        # self.mutation()
        # self.replace_population()

        # Return the best individual or other desired output
        pass

    # Selection schemes
    def fitness_proportionate_selection(self):
        pass

    def rank_based_selection(self):
        pass

    def binary_tournament_selection(self):
        pass

    def truncation_selection(self):
        pass

    def random_selection(self):
        pass
