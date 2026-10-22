import json
import pennylane as qp
import pennylane.numpy as np

# Write any helper functions you need here

def symmetry_score(data, labels, s):
    """This function returns the data's symmetry score for a given symmetry s
    
    Args:
        data (np.array): An array containing binary arrays, which represent the data points
        labels (np.array(int)): The label for each data point. There may be more than two labels.
        s (np.array): A binary array representing the candidate symmetry.

    Returns:
        (float): The symmetry score, as described in the challenge statement.
    """

    s_t = tuple(int(v) for v in s)
    points = [tuple(int(v) for v in x) for x in data]
    labs = [int(l) for l in labels]
    N = len(points)

    score = 0.0
    for r in set(labs):
        X_r = {p for p, l in zip(points, labs) if l == r}
        paired = sum(1 for x in X_r if tuple((a + b) % 2 for a, b in zip(x, s_t)) in X_r)
        p_r = 0.5 * (1 + paired / len(X_r))
        score += len(X_r) / N * p_r

    return float(score)

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    data, labels, s = json.loads(test_case_input)[0], json.loads(test_case_input)[1], json.loads(test_case_input)[2]
    data = np.array(data)
    labels = np.array(labels)
    s = np.array(s)
    out = symmetry_score(data, labels, s)
    return str(out)


def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
                                 
    assert np.isclose(solution_output, expected_output, rtol=1e-3)

# These are the public test cases
test_cases = [
    ('[[[0, 0, 0], [1, 1, 0], [0, 0, 1], [1, 1, 1], [1, 0, 1]], [0, 0, 1, 1, 2], [1,1,0]]', '0.9'),
    ('[[[0, 0, 0], [1, 1, 0], [0, 0, 1]], [0, 0, 0], [1,1,0]]', '0.833333333333333')
]

# This will run the public test cases locally
for i, (input_, expected_output) in enumerate(test_cases):
    print(f"Running test case {i} with input '{input_}'...")

    try:
        output = run(input_)

    except Exception as exc:
        print(f"Runtime Error. {exc}")

    else:
        if message := check(output, expected_output):
            print(f"Wrong Answer. Have: '{output}'. Want: '{expected_output}'.")

        else:
            print("Correct!")
