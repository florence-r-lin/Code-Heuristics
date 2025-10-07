
# Run the metrics function on LOC.py
from HardMetrics import allMetrics

for i in range(10000):
    result = allMetrics("/Users/summer-2024/Code-Heuristics/measurables/testing files/LOC.py")
print("Metrics for LOC.py:")
print(result)
