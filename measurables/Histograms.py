import matplotlib.pyplot as plt
import numpy as np
import os
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
    plt.ylabel('Frequency' if not fitLine else 'Density', fontsize=14)
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


def makeMulHistograms(data_dict, num_bins, titles = None, colors = None, fitLine=True, output_dir=None, year=None, statsCsv=None):
    num_histograms = len(data_dict)
    fig, axes = plt.subplots(1, num_histograms, figsize=(20, 5), constrained_layout=True)
    
    for ax, (title, data), bins, color in zip(axes, data_dict.items(), num_bins, colors):
        makeHistogram(data, numBins=bins, graphName=title, xaxis=title, color=color,
                      fitLine=fitLine, filename=f"{title.lower().replace(' ', '_')}_histogram_{year}.png",
                      csv_filename=statsCsv, output_dir=output_dir, ax=ax)
    
    plt.show()

