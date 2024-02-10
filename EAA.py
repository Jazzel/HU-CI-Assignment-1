import random

from main import EvolutionaryAlgorithm
from PIL import Image, ImageDraw
import numpy as np

IMAGE_WIDTH = 800
IMAGE_HEIGHT = 800


class EAA(EvolutionaryAlgorithm):

    def __init__(
        self,
        parent_selection_scheme,
        survival_selection_scheme,
        population_size,
        no_of_generations,
        no_of_offsprings,
        mutation_rate,
        no_of_iterations,
        num_polygons,
        max_vertices,
        target_human_image,
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
        self.num_polygons = num_polygons
        self.max_vertices = max_vertices
        self.parent_selection_scheme = parent_selection_scheme
        self.survival_selection_scheme = survival_selection_scheme
        self.no_of_offsprings = no_of_offsprings
        self.population_size = population_size
        self.no_of_generations = no_of_generations
        self.no_of_offsprings = no_of_offsprings
        self.mutation_rate = mutation_rate
        self.no_of_iterations = no_of_iterations
        self.target_human_image = target_human_image

        # self.comment = ""
        # self.operations = []
        # self.distance_matrix = []

        self.counter = 0

        self.read_file()

    def read_file(self):
        image = Image.open(self.target_human_image)
        image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        self.target_human_image = image
        # image.show()

    def chromosome(self) -> list:
        chromosome = []
        for _ in range(self.num_polygons):
            num_vertices = random.randint(3, self.max_vertices)
            polygon = {
                "vertices": [
                    (random.randint(0, IMAGE_WIDTH), random.randint(0, IMAGE_HEIGHT))
                    for _ in range(num_vertices)
                ],
                "color": (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                ),
                "transparency": random.uniform(0.1, 0.9),
            }
            chromosome.append(polygon)
        return chromosome

    def compute_fitness(self, rendered_image, target_human_image) -> float:

        rendered_array = np.array(rendered_image)
        target_array = np.array(target_human_image)

        diff = np.sum(np.abs(rendered_array - target_array))

        normalized_diff = diff / (
            self.target_human_image.size[0] * self.target_human_image.size[1] * 3 * 255
        )

        return normalized_diff

    def evaluate_fitness(self, chromosome) -> float:
        rendered_image = self.render_individual(
            chromosome, self.target_human_image.size
        )

        return self.compute_fitness(rendered_image, self.target_human_image)

    def compute_population_fitness(self, population: dict) -> dict:
        fitness_dictionary = {}
        for individual, chromosome in population.items():
            fitness_dictionary[individual] = self.evaluate_fitness(chromosome)
        return fitness_dictionary

    def render_individual(self, chromosome, image_size) -> Image:
        image = Image.new("RGB", image_size, color="white")
        draw = ImageDraw.Draw(image)

        for polygon in chromosome:
            vertices = [(x, y) for x, y in polygon["vertices"]]
            color = tuple(polygon["color"])
            transparency = int(255 * polygon["transparency"])
            draw.polygon(vertices, fill=color + (transparency,))

        image.save(f"images/image_{self.counter}.png")
        self.counter += 1
        # image.show()

        return image


population_size = 30
no_of_offsprings = 10
no_of_generations = 20000
mutation_rate = 0.5
no_of_iterations = 10
parent_selection = 2
survival_selection = 4
num_polygons = 50
max_vertices = 6
target_human_image = "mona_lisa.jpg"

eaa = EAA(
    parent_selection_scheme=parent_selection,
    survival_selection_scheme=survival_selection,
    population_size=population_size,
    no_of_generations=no_of_generations,
    no_of_offsprings=no_of_offsprings,
    mutation_rate=mutation_rate,
    no_of_iterations=no_of_iterations,
    num_polygons=num_polygons,
    max_vertices=max_vertices,
    target_human_image=target_human_image,
)
eaa.run()
# eaa.read_file()
# ch = eaa.chromosome()
# print(eaa.initialize_population())
# print(eaa.chromosome())

# eaa.run()
