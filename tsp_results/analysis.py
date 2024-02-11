import json
import pandas as pd
import matplotlib.pyplot as plt

files = [
    "tsp_qa194.tsp_p1_s2.json",
    "tsp_qa194.tsp_p1_s4.json",
    "tsp_qa194.tsp_p1_s5.json",
    "tsp_qa194.tsp_p2_s4.json",
    "tsp_qa194.tsp_p3_s4.json",
    "tsp_qa194.tsp_p4_s4.json",
    "tsp_qa194.tsp_p5_s5.json",
]

for file in files:

    algo = file.split(".")[1]
    parent = algo.split("_")[1]
    surviver = algo.split("_")[2]

    if parent == "p1":
        parent = "Fitness-Proportional"
    elif parent == "p2":
        parent = "Rank-Based"
    elif parent == "p3":
        parent = "Tournament"
    elif parent == "p4":
        parent = "Truncation"
    elif parent == "p5":
        parent = "Random"

    if surviver == "s1":
        surviver = "Fitness-Proportional"
    elif surviver == "s2":
        surviver = "Rank-Based"
    elif surviver == "s3":
        surviver = "Tournament"
    elif surviver == "s4":
        surviver = "Truncation"
    elif surviver == "s5":
        surviver = "Random"

    df = pd.DataFrame()
    results = pd.DataFrame()
    with open(file, "r") as f:
        data = json.load(f)

        rows = []

        for iteration, generation_data in data.items():
            iteration_number = int(iteration)
            for generation_info in generation_data:
                generation_number = generation_info["generation"]
                average = generation_info["average"]
                best = generation_info["best"]
                best_chromosome = generation_info["best_chromosome"]

                row = {
                    "iteration": iteration_number,
                    "generation": generation_number,
                    "average": average,
                    "best": best,
                    "best_chromosome": best_chromosome,
                }
                rows.append(row)

        df = pd.DataFrame(rows)

        pivot_df = df.pivot_table(
            index="generation", columns=["iteration"], values=["average", "best"]
        )

        avg_of_avgs = df.groupby(["generation"])["average"].mean()
        min_avg_of_avgs = avg_of_avgs.min()
        max_avg_of_avgs = avg_of_avgs.max()
        avg_of_best = df.groupby(["generation"])["best"].mean()
        min_avg_of_best = avg_of_best.min()
        max_avg_of_best = avg_of_best.max()
        pivot_df["Average of averages"] = avg_of_avgs
        pivot_df["Average of Best"] = avg_of_best

        avg_df = pd.DataFrame(
            {
                "generation": avg_of_avgs.index,
                "avg_of_avgs": avg_of_avgs.values,
                "avg_of_best": avg_of_best.values,
            }
        )

        print(f"Parent: {parent}, Surviver: {surviver}")
        print(avg_df[avg_df["generation"] == 0])
        print(avg_df[avg_df["generation"] == 10000])

        avg_df.plot(y=["avg_of_avgs", "avg_of_best"], linestyle="-", figsize=(10, 5))
        plt.xlabel("Generation")
        plt.ylabel("Fitness")

        plt.title(f"Parent: {parent}, Surviver: {surviver}")
        plt.legend(["Average of averages", "Average of best"])
        plt.grid(True)
        plt.tight_layout()

        plt.savefig(file.split(".")[1] + ".png")

        f.close()
