import matplotlib.pyplot as plt

def makeHistogram(inputList, numBins = range(0,10), graphName = '', xaxis = ''):
    plt.hist(inputList, numBins, edgecolor='black')
    plt.title(graphName)
    plt.xlabel(xaxis)
    plt.ylabel('Frequency')
    plt.show()
