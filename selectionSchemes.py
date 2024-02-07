import random


    # Selection schemes
class SelectionScheme:

    def fitness_proportionate_selection(self, selection_size) -> list:
        total_fitness = sum( 1/individual_fitness for individual_fitness in self.fitness_dictionary.values())
        probabilities = [
            ((1/fitness) / total_fitness) for fitness in self.fitness_dictionary.values()
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
