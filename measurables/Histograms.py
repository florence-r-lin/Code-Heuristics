import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import pandas as pd  # Make sure to import pandas for CSV handling

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
                  fitLine=True, filename=None, csv_filename=None, display_stats=True):
    
    if isinstance(color, tuple) and all(0 <= val <= 255 for val in color):
        color = tuple(val / 255 for val in color)
    
    # Calculate statistics
    mean = round(np.mean(inputList), 2)  
    median = round(np.median(inputList),2) 
    std_dev = round(np.std(inputList),2) 

    # Generate histogram
    plt.figure(figsize=(8, 6))
    counts, bins, patches = plt.hist(inputList, numBins, edgecolor='black', color=color, density=True)

    # Overlay fitted Gaussian curve if fitLine=True
    if fitLine:
        # mean, std_dev = norm.fit(inputList)
        x_values = np.linspace(min(bins), max(bins), 100)
        fitted_curve = norm.pdf(x_values, mean, std_dev)
        plt.plot(x_values, fitted_curve, color='red', linestyle='--', linewidth=2, label = None)


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
                       bbox=dict(boxstyle='round,pad=0.3', edgecolor='white', facecolor='lightgrey', alpha = 0))

    plt.tight_layout()
    
    # Save the figure to a file if a filename is provided
    if filename:
        plt.savefig(filename, format='png')  # Save the figure with the fitted curve included
    
    plt.show()  # Show the plot

    # Write statistics to CSV if csv_filename is provided
    if csv_filename:
        # Prepare data for the CSV
        stats_data = {
            'Graph Name': [graphName],
            'Mean': [mean],
            'Median': [median],
            'Std Dev': [std_dev]
        }
        
        # Create a DataFrame from the stats_data
        stats_df = pd.DataFrame(stats_data)
        stats_df.to_csv(csv_filename, mode='a', header=False, index=False)

