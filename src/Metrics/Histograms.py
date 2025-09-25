import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import math
from scipy.stats import norm
#import pandas as pd  # Make sure to import pandas for CSV handling
import pandas as pd
# Update default font settings for better aesthetics
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 14,
    'axes.titleweight': 'bold',
    'axes.labelweight': 'bold',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'xtick.direction': 'in',
    'ytick.direction': 'in'
})

def makeHistogram(inputList, numBins=10, graphName='', xaxis='', color=(148, 181, 242), 
                  fitLine=True, filename=None, csv_filename=None, display_stats=True, output_dir=None):

    # Ensure color is normalized to [0, 1]
    if isinstance(color, tuple) and all(0 <= val <= 255 for val in color):
        color = tuple(val / 255 for val in color)
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Calculate statistics
    mean = round(np.mean(inputList), 2)  
    median = round(np.median(inputList), 2) 
    std_dev = round(np.std(inputList), 2) 

    # Generate histogram
    plt.figure(figsize=(8, 6))
    counts, bins, patches = plt.hist(inputList, numBins, edgecolor='black', color=color, density=True)

    # Overlay fitted Gaussian curve if fitLine=True
    if fitLine:
        x_values = np.linspace(min(bins), max(bins), 100)
        fitted_curve = norm.pdf(x_values, mean, std_dev)
        plt.plot(x_values, fitted_curve, color='red', linestyle='--', linewidth=2, label=None)

    # Set titles and labels with improved aesthetics
    plt.title(graphName, fontsize=18, weight='bold')
    plt.xlabel(xaxis, fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add statistics text to the plot if display_stats is True
    if display_stats:
        stats_text = (f'Mean: {mean}\n'
                      f'Median: {median}\n'
                      f'Std Dev: {std_dev}')
        plt.gca().text(0.95, 0.95, stats_text, fontsize=10, ha='right', va='top', transform=plt.gca().transAxes,
                       bbox=dict(boxstyle='round,pad=0.3', edgecolor='white', facecolor='lightgrey', alpha=0))

    plt.tight_layout()

    # Save the figure to the specified directory
    if filename:
        save_path = os.path.join(output_dir, filename)
        plt.savefig(save_path, format='png')  # Save the figure with the fitted curve included

    plt.show()  # Show the plot

    # Write statistics to CSV if csv_filename is provided
    if csv_filename:
        stats_data = {
            'Graph Name': [graphName],
            'Mean': [mean],
            'Median': [median],
            'Std Dev': [std_dev]
        }
        stats_df = pd.DataFrame(stats_data)
        stats_df.to_csv(os.path.join(output_dir, csv_filename), mode='a', header=False, index=False)

def makeMultipleHistograms(inputList, numBins, graphName, xaxis, color, fitLine, filename, output_dir):
    num_histograms = len(inputList)
    num_cols = 2  # Fixed to 2 columns
    num_rows = (num_histograms + 1) // num_cols  # Calculate rows needed for 2 columns

    # Create subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 5 * num_rows), squeeze=False)

    for i, data in enumerate(inputList):
        ax = axes[i // num_cols][i % num_cols]
        bins = numBins[i]
        title = graphName[i]
        xlabel = xaxis[i]
        current_color = tuple(val / 255 for val in color[i])
        show_fit = fitLine[i]

        # Plot histogram
        counts, bins, patches = ax.hist(data, bins=bins, edgecolor='black', color=current_color, density=True)

        # Add a fit line if required
        if show_fit:
            mean = np.mean(data)
            std_dev = np.std(data)
            x_values = np.linspace(min(bins), max(bins), 100)
            fitted_curve = norm.pdf(x_values, mean, std_dev)
            ax.plot(x_values, fitted_curve, color='red', linestyle='--', linewidth=2)

        # Add titles and labels
        ax.set_title(title, fontsize=14, weight='bold')
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Hide unused subplots
    for j in range(num_histograms, num_rows * num_cols):
        axes[j // num_cols][j % num_cols].axis('off')

    # Adjust layout
    plt.tight_layout()

    # Save the figure
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        save_path = os.path.join(output_dir, f"{filename}.png")
    else:
        save_path = f"{filename}.png"
    plt.savefig(save_path)
    plt.show()