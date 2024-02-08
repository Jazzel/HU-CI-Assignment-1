import random

from main import EvolutionaryAlgorithm


class JSSP(EvolutionaryAlgorithm):

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
        self.comment = ""
        self.operations = []
        self.distance_matrix = []
        self.read_file()

    def read_file(self):
        with open(self.filename, "r") as f:
            self.comment = f.readline().strip()
            self.operations = f.readline().strip().split()
            total_machines = int(self.operations[0])
            total_jobs = int(self.operations[1])
            line = f.readline().strip()
            self.operations_data = {}
            job_no = 0
            while True:
                try:
                    raw_data = line.split()
                    for i in range(0,len(raw_data),2):
                        self.operations_data[(job_no,raw_data[i])] = [raw_data]
                    line = f.readline().strip()
                    job +=1 
                except EOFError:
                    break
    
    def chromosome(self) -> list:
        temp = list(self.operations_data.keys())
        arr = [i for i in temp]
        random.shuffle(arr)
        return arr

    def fitness(self, chromosome: list) -> float:
        pass

filename = "abz5.txt"
population_size = 30
no_of_offsprings = 10
no_of_generations = 20000
mutation_rate = 0.5
no_of_iterations = 10
parent_selection = 2
survival_selection = 2

jssp = JSSP(
    filename=filename,
    parent_selection_scheme=parent_selection,
    survival_selection_scheme=survival_selection,
    population_size=population_size,
    no_of_generations=no_of_generations,
    no_of_offsprings=no_of_offsprings,
    mutation_rate=mutation_rate,
    no_of_iterations=no_of_iterations,
)
jssp.run()
# data = {
#     0: [
#         (4, 88),
#         (8, 68),
#         (6, 94),
#         (5, 99),
#         (1, 67),
#         (2, 89),
#         (9, 77),
#         (7, 99),
#         (0, 86),
#         (3, 92),
#     ],
#     1: [
#         (5, 72),
#         (3, 50),
#         (6, 69),
#         (4, 75),
#         (2, 94),
#         (8, 66),
#         (0, 92),
#         (1, 82),
#         (7, 94),
#         (9, 63),
#     ],
#     2: [
#         (9, 83),
#         (8, 61),
#         (0, 83),
#         (1, 65),
#         (6, 64),
#         (5, 85),
#         (7, 78),
#         (4, 85),
#         (2, 55),
#         (3, 77),
#     ],
#     3: [
#         (7, 94),
#         (2, 68),
#         (1, 61),
#         (4, 99),
#         (3, 54),
#         (6, 75),
#         (5, 66),
#         (0, 76),
#         (9, 63),
#         (8, 67),
#     ],
#     4: [
#         (3, 69),
#         (4, 88),
#         (9, 82),
#         (8, 95),
#         (0, 99),
#         (2, 67),
#         (6, 95),
#         (5, 68),
#         (7, 67),
#         (1, 86),
#     ],
#     5: [
#         (1, 99),
#         (4, 81),
#         (5, 64),
#         (6, 66),
#         (8, 80),
#         (2, 80),
#         (7, 69),
#         (9, 62),
#         (3, 79),
#         (0, 88),
#     ],
#     6: [
#         (7, 50),
#         (1, 86),
#         (4, 97),
#         (3, 96),
#         (0, 95),
#         (8, 97),
#         (2, 66),
#         (5, 99),
#         (6, 52),
#         (9, 71),
#     ],
#     7: [
#         (4, 98),
#         (6, 73),
#         (3, 82),
#         (2, 51),
#         (1, 71),
#         (5, 94),
#         (7, 85),
#         (0, 62),
#         (8, 95),
#         (9, 79),
#     ],
#     8: [
#         (0, 94),
#         (6, 71),
#         (3, 81),
#         (7, 85),
#         (1, 66),
#         (2, 90),
#         (4, 76),
#         (5, 58),
#         (8, 93),
#         (9, 97),
#     ],
#     9: [
#         (3, 50),
#         (0, 59),
#         (1, 82),
#         (8, 67),
#         (7, 56),
#         (9, 96),
#         (6, 58),
#         (4, 81),
#         (5, 59),
#         (2, 96),
#     ],
# }

# # operations = [(job, machine) for job, jobData in self.data.items() for machine, _ in jobData]

# operations = {}
# processings = {}
# for job, jobData in data.items():
#     # print(job, jobData)
#     operations[job] = []
#     processings[job] = {}
#     for machine, time in jobData:
#         operations[job].append(machine)
#         processings[job][machine] = time

# print(operations)
# print(processings)