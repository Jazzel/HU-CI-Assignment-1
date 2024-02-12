import random
import numpy as np
from selectionSchemes import SelectionScheme


class EvolutionaryAlgorithm(SelectionScheme):
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
        parent_selection_scheme: int = 1,
        survival_selection_scheme: int = 1,
        population_size: int = 30,
        no_of_generations: int = 50,
        no_of_offsprings: int = 10,
        mutation_rate: float = 0.5,
        no_of_iterations: int = 10,
    ) -> None:
        self.population_size = population_size
        self.no_of_offsprings = no_of_offsprings
        self.no_of_generations = no_of_generations
        self.mutation_rate = mutation_rate
        self.no_of_iterations = no_of_iterations
        self.parent_selection_scheme = parent_selection_scheme
        self.survivor_selection_scheme = survival_selection_scheme

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
        self.offsprings = {}

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
        d_index = len(self.population)
        for index in range(0, len(self.parents), 2):

            # print("Parents: ", len(self.parents))

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

            self.offsprings[d_index] = offspring1
            self.offsprings[d_index + 1] = offspring2
            d_index += 2

    def mutation(self) -> None:
        if random.random() < self.mutation_rate:
            for individual in self.offsprings.keys():
                index1 = random.randint(0, len(self.offsprings[individual]) - 1)
                index2 = random.randint(0, len(self.offsprings[individual]) - 1)
                (
                    self.offsprings[individual][index1],
                    self.offsprings[individual][index2],
                ) = (
                    self.offsprings[individual][index2],
                    self.offsprings[individual][index1],
                )

    def survivor_selection(self) -> None:
        """
        Performs selection to choose parents for reproduction.
        """
        survivers = []
        if self.survivor_selection_scheme == 1:
            survivers = self.fitness_proportionate_selection(self.population_size - 1)
        elif self.survivor_selection_scheme == 2:
            survivers = self.rank_based_selection(self.population_size - 1)
        elif self.survivor_selection_scheme == 3:
            survivers = self.binary_tournament_selection(self.population_size - 1)
        elif self.survivor_selection_scheme == 4:
            survivers = self.truncation_selection(self.population_size - 1)
        elif self.survivor_selection_scheme == 5:
            survivers = self.random_selection(self.population_size - 1)
        else:
            print("Invalid selection scheme")

        updatedPopulation = []
        for index in survivers:
            updatedPopulation.append(self.population[index])
        self.population = {
            i: updatedPopulation[i] for i in range(len(updatedPopulation))
        }

    def run(self):
        # Run the evolutionary algorithm
        iteration = 1
        fitttest_individual = []
        fitnesses = []
        self.initialize_population()
        while iteration <= self.no_of_generations:
            # while iteration <= 2:
            print(f"Iteration {iteration}")
            # print("population:", len(self.population))
            self.fitness_dictionary = self.compute_population_fitness(self.population)
            # print("fitness_dictionary:", len(self.fitness_dictionary))

            fittest_individual = self.population[
                min(self.fitness_dictionary, key=self.fitness_dictionary.get)
            ]
            self.parent_selection()
            # print("parents:", len(self.parents))
            self.crossover()
            self.mutation()
            # print("offsprings:", len(self.offsprings))

            updatedPopulation = list(self.population.values()) + list(
                self.offsprings.values()
            )

            self.population = {
                i: updatedPopulation[i] for i in range(0, len(updatedPopulation))
            }

            self.fitness_dictionary = self.compute_population_fitness(self.population)

            # print(
            #     "fitness_dictionary (offsprings added):", len(self.fitness_dictionary)
            # )
            # print("population (offsprings added):", len(self.fitness_dictionary))
            self.survivor_selection()
            self.population[len(self.population)] = fittest_individual

            self.fitness_dictionary = self.compute_population_fitness(self.population)

            # print("population (survivors):", len(self.population))
            # print(self.fitness_dictionary.values())
            avg_fitness = np.array(list(self.fitness_dictionary.values())).mean()
            fitnesses.append(avg_fitness)
            print(
                "avg_fitness:",
                avg_fitness,
                "fittest:",
                min(self.fitness_dictionary.values()),
            )

            # TODO: remove for TSP, JSSP
            fittest = min(self.fitness_dictionary, key=self.fitness_dictionary.get)
            if iteration % 50 == 0 :
                self.save_image(
                    self.population[fittest],
                    (200, 200),
                    f"generation_{iteration}_fittest",
                )

            iteration += 1

        print(min(fitnesses))
        print(max(fitnesses))

