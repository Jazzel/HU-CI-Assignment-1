import pandas as pd
import matplotlib.pyplot as plt

data = #...chromosome

# Convert data to a format suitable for DataFrame
formatted_data = [
    (job, machine, start, end) for (job, machine), (start, end) in data.items()
]
df = pd.DataFrame(formatted_data, columns=["Job", "Machine", "Start", "End"])

# Create a Gantt chart
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the bars
for row in df.itertuples(index=False):
    ax.barh(
        y=row.Machine,
        width=row.End - row.Start,
        left=row.Start,
        height=0.5,
        align="center",
        alpha=0.6,
    )

# Set labels and title
ax.set_xlabel("Time")
ax.set_ylabel("Machine")
ax.set_title("Gantt Chart")

# Show grid
ax.grid(True)

plt.show()
