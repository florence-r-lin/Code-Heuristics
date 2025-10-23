import Submission
import applyMetrics

def test_one():
    path = "/Users/summer-2024/Code-Heuristics/tests/example testing files/LOC.py"
    sub = Submission.Submission(path)
    metrics = sub.get_metrics()
    row = applyMetrics._to_row(metrics)
    print(row)

test_one()
