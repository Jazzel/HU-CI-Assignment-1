import random

from main import EvolutionaryAlgorithm
from PIL import Image, ImageDraw, ImageChops
import numpy as np

IMAGE_WIDTH = 200
IMAGE_HEIGHT = 200


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

        # Convert the image to RGB mode
        target_image = image.convert("RGB")

        # Get the image data as a numpy array
        image_array = np.array(target_image)

        # Reshape the image data to a 2D array of pixels (rows) x RGB values (columns)
        pixels = image_array.reshape(-1, 3)

        # Randomly sample colors or use clustering algorithm to find dominant colors
        unique_colors = np.unique(pixels, axis=0)

        self.target_image_colors = unique_colors.tolist()

        # image.show()

    def chromosome(self) -> list:
        chromosome = []
        for _ in range(self.num_polygons):
            num_vertices = random.randint(3, self.max_vertices)
            color = random.choice(self.target_image_colors)
            polygon = {
                "vertices": [
                    (random.randint(0, IMAGE_WIDTH), random.randint(0, IMAGE_HEIGHT))
                    for _ in range(num_vertices)
                ],
                "color": color,
                "transparency": float(0.5),
            }
            chromosome.append(polygon)
        return chromosome

    def compute_fitness(self, rendered_image, target_human_image) -> float:
        diff = ImageChops.difference(rendered_image, target_human_image)
        totdiff = np.array(diff.getdata()).sum()

        return totdiff

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
        draw = ImageDraw.Draw(image,"RGBA")
        for polygon in chromosome:
            vertices = [(x, y) for x, y in polygon["vertices"]]
            color = tuple(polygon["color"])
            transparency = int(255 * polygon["transparency"])
            draw.polygon(vertices, fill=color + (transparency,))

        # image.save(f"images/image_{self.counter}.png")
        self.counter += 1
        # image.show()

        return image

    def save_image(self, chromosome, image_size, filename) -> Image:
        image = Image.new("RGB", image_size, color="white")
        draw = ImageDraw.Draw(image,"RGBA")
        for polygon in chromosome:
            vertices = [(x, y) for x, y in polygon["vertices"]]
            color = tuple(polygon["color"])
            transparency = int(255 * polygon["transparency"])
            draw.polygon(vertices, fill=color + (transparency,))

        image.save("images3/" + filename + ".png")

    def mutation(self) -> None:
        if random.random() < self.mutation_rate:
            num_vertices = random.randint(3, self.max_vertices)
            for individual in self.offsprings.keys():
                index1 = random.randint(0, len(self.offsprings[individual]) - 1)
                index2 = random.randint(0, len(self.offsprings[individual]) - 1)
                self.offsprings[individual][index1] = {
                    "vertices": [
                        (random.randint(0, IMAGE_WIDTH), random.randint(0, IMAGE_HEIGHT))
                        for _ in range(num_vertices)
                    ],
                    "color": random.choice(self.target_image_colors),
                    "transparency": float(0.5),
                    }
                self.offsprings[individual][index2] = {
                    "vertices": [
                        (random.randint(0, IMAGE_WIDTH), random.randint(0, IMAGE_HEIGHT))
                        for _ in range(num_vertices)
                    ],
                    "color": random.choice(self.target_image_colors),
                    "transparency": float(0.5),
                    }
                
population_size = 10
no_of_offsprings = 10
no_of_generations = 10000
mutation_rate = 1
no_of_iterations = 1
parent_selection = 1
survival_selection = 4
num_polygons = 50
max_vertices = 6
target_human_image = "tom_jerry.jpg"

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
