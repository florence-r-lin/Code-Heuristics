import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

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

def makeHistogram(inputList, numBins=10, graphName='', xaxis='', color=(148, 181, 242), fitLine=True, filename=None):
    # Normalize RGB values if provided as a tuple with values from 0 to 255
    if isinstance(color, tuple) and all(0 <= val <= 255 for val in color):
        color = tuple(val / 255 for val in color)
    
    # Generate histogram
    plt.figure(figsize=(8, 6))
    counts, bins, patches = plt.hist(inputList, numBins, edgecolor='black', color=color, density=True)
    
    # Overlay fitted Gaussian curve if fitLine=True
    if fitLine:
        mean, std_dev = norm.fit(inputList)
        x_values = np.linspace(min(bins), max(bins), 100)
        fitted_curve = norm.pdf(x_values, mean, std_dev)
        plt.plot(x_values, fitted_curve, color='red', linestyle='--', linewidth=2, label='Fitted Gaussian')
        plt.legend()

    # Set titles and labels with improved aesthetics
    plt.title(graphName, fontsize=18, weight='bold')
    plt.xlabel(xaxis, fontsize=14)
    plt.ylabel('Frequency' if not fitLine else 'Density', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Save the figure to a file if a filename is provided
    if filename:
        plt.savefig(filename, format='png')  # Save the figure with the fitted curve included
    
    plt.show()  # Show the plot
