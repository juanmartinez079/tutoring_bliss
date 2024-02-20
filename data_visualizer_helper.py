import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import FuncFormatter


def bar_plot_visualization(dataset, datalabels):
    longest = max([len(data) for data in dataset])

    fig, axs = plt.subplots(len(dataset), 1, figsize=(longest, 2.75 * len(dataset)))

    def animate(frame):
        for data, bars in zip(dataset, bar_plots):
            heights = [frame * v / 50 for v in list(data.values())]
            for bar, height in zip(bars.patches, heights):
                bar.set_height(frame * height / 50)

    bar_plots = []  # List to store the bar plots

    for i, data in enumerate(dataset):
        ax = axs[i] if len(dataset) > 1 else axs  # If only one dataset, use the single axis

        # Determine the minimum and maximum heights of the bars
        min_height = min(data.values())
        max_height = max(data.values())

        # Normalize the heights to the range [0, 1]
        normalized_heights = [(height - min_height) / (max_height - min_height) for height in data.values()]

        # Create a color gradient from red to green based on the normalized heights
        colors = sns.color_palette("RdYlGn", len(data))
        custom_colors = [colors[int(height * (len(colors) - 1))] for height in normalized_heights]

        # Visualization
        bars = sns.barplot(x=list(data.keys()), y=[0] * len(data), ax=ax, palette=custom_colors)
        bar_plots.append(bars)

        # Set the capstyle property of the bar objects to 'round' to make the corners rounded
        # Make the corners of the bars rounded by setting edgecolor and linewidth
        for patch, height in zip(bars.patches, data.values()):
            ax.text(patch.get_x() + patch.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')

        plt.xlabel('Payee')
        plt.ylabel('Total ($)')

        if len(data) > 5:
            ax.tick_params(labelrotation=45, size=1)
        else:
            ax.tick_params(size=1)
        ax.set_title(datalabels[i])  # Set the title for the subplot

        # Set the y-axis limits to start from 0 and end at the maximum payee total
        ax.set_ylim(0, max(data.values()) * 1.25)  # Add some padding to the top

    anim = FuncAnimation(fig, animate, frames=50, interval=1, repeat=False)

    plt.tight_layout()

    plt.show()


def pie_chart_visualization(data):
    # Create a pie chart
    fig, ax = plt.subplots()
    wedges, _ = ax.pie(data.values(), labels=data.keys(), wedgeprops=dict(width=0.4))

    # Function to update the pie chart with animation
    def update(frame):
        for wedge, frac in zip(wedges, data.values()):
            wedge.set_width(0.4 * frame / 50)

    # Create the animation
    anim = FuncAnimation(fig, update, frames=300, interval=1, repeat=False)

    plt.show()
    print('done')
