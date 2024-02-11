import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

files = [
    # "jssp_abz5.txt_p1_s2.json",
    # "jssp_abz5.txt_p1_s4.json",
    # "jssp_abz5.txt_p3_s4.json",
    # "jssp_abz5.txt_p4_s4.json",
    # "jssp_abz5.txt_p5_s5.json",
    # "jssp_abz6.txt_p1_s2.json",
    # "jssp_abz6.txt_p1_s4.json",
    # "jssp_abz6.txt_p3_s4.json",
    # "jssp_abz6.txt_p4_s4.json",
    # "jssp_abz6.txt_p5_s5.json",
    "jssp_abz7.txt_p1_s2.json",
    "jssp_abz7.txt_p1_s4.json",
    "jssp_abz7.txt_p3_s4.json",
    "jssp_abz7.txt_p4_s4.json",
    "jssp_abz7.txt_p5_s5.json",
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
    pivot_df = pd.DataFrame()
    with open(file, "r") as f:
        data = json.load(f)

        rows = []

        for iteration, generation_data in data.items():
            iteration_number = int(iteration)
            for generation_info in generation_data:
                generation_number = generation_info["generation"]
                average = generation_info["average"]
                best = generation_info["best"]
                best_chromosome = generation_info["best_chromesome"]

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
            index="generation",
            columns=["iteration"],
            values=["average", "best", "best_chromosome"],
            aggfunc="first",
        )

        avg_of_avgs = df.groupby(["generation"])["average"].mean()
        avg_of_best = df.groupby(["generation"])["best"].mean()
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
        print(avg_df[avg_df["generation"] == 5000])

        avg_df.plot(y=["avg_of_avgs", "avg_of_best"], linestyle="-", figsize=(10, 5))
        plt.xlabel("Generation")
        plt.ylabel("Fitness")

        plt.title(f"Parent: {parent}, Surviver: {surviver}")
        plt.legend(["Average of averages", "Average of best"])

        plt.savefig(".".join(file.split(".")[0:2]) + ".png")

        minimum_avg_best = pivot_df["Average of Best"].idxmin()

        min_row = pivot_df.loc[minimum_avg_best]

        # Get the best chromosome corresponding to the minimum value
        best_chromosome_of_min_best = min_row["best_chromosome"].values[0]
        plot_data = {}
        for data in best_chromosome_of_min_best.values():
            plot_data[(data[0], data[1])] = [data[2], data[3]]

        # Convert data to a format suitable for DataFrame
        formatted_data = [
            (job, machine, start, end)
            for (job, machine), (start, end) in plot_data.items()
        ]
        df = pd.DataFrame(formatted_data, columns=["Job", "Machine", "Start", "End"])

        # Get unique jobs
        unique_jobs = df["Job"].unique()

        # Generate unique colors for each job
        colors = plt.cm.tab10(np.linspace(0, 1, len(unique_jobs)))

        # Map each job to a unique color
        job_colors = {job: color for job, color in zip(unique_jobs, colors)}

        # Create a Gantt chart
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot the bars with unique colors
        for row in df.itertuples(index=False):
            ax.barh(
                y=row.Machine,
                width=row.End - row.Start,
                left=row.Start,
                height=0.5,
                align="center",
                alpha=0.6,
                color=job_colors[row.Job],
            )

        # Set labels and title
        ax.set_xlabel("Time")
        ax.set_ylabel("Machine")
        ax.set_title(f"Best Chromosome | Parent: {parent}, Surviver: {surviver}")

        # Show grid
        ax.grid(True)

        plt.savefig(".".join(file.split(".")[0:2]) + "_gantt_chart.png")

        f.close()
