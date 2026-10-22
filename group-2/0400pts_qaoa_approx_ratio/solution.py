import json
import pennylane as qp
import pennylane.numpy as np

def build_cost_hamiltonian(edges, n_wires):
    """H_cost = 3/4 * sum_{(i,j)} (Z_i Z_j + Z_i + Z_j) - sum_i Z_i"""
    coeffs, ops = [], []
    for i, j in edges:
        coeffs += [0.75, 0.75, 0.75]
        ops += [qp.PauliZ(i) @ qp.PauliZ(j), qp.PauliZ(i), qp.PauliZ(j)]
    for i in range(n_wires):
        coeffs.append(-1.0)
        ops.append(qp.PauliZ(i))
    return qp.Hamiltonian(coeffs, ops)


def classical_min_energy(edges, n_wires):
    """Exact minimum eigenvalue of the diagonal cost Hamiltonian (brute force)."""
    best = np.inf
    for b in range(2 ** n_wires):
        z = [1 - 2 * ((b >> k) & 1) for k in range(n_wires)]  # bit 1 -> Z = -1
        energy = sum(0.75 * (z[i] * z[j] + z[i] + z[j]) for i, j in edges) - sum(z)
        best = min(best, energy)
    return float(best)


def qaoa_layer(gamma, alpha, edges, n_wires):
    # Cost unitary exp(-i * gamma * H_cost); all terms commute, so this is exact
    for i, j in edges:
        qp.IsingZZ(2 * gamma * 0.75, wires=[i, j])
        qp.RZ(2 * gamma * 0.75, wires=i)
        qp.RZ(2 * gamma * 0.75, wires=j)
    for i in range(n_wires):
        qp.RZ(2 * gamma * (-1.0), wires=i)
    # Mixer unitary exp(-i * alpha * sum X_i)
    for i in range(n_wires):
        qp.RX(2 * alpha, wires=i)

def approximation_ratio(edges):

    """This function calculates the approximation ratio of QAOA for
    the minimum vertex cover problem

    Args:
    - Edges (list(list(int))): A list of ordered pairs of integers, representing 
    the edges of the graph for which we need to solve the minimum vertex cover problem.

    Returns:
    - np.tensor(float): The approximation ratio of QAOA for the minimum vertex cover problem for
    the input graph.
    """

    # Write your QAOA circuit and optimization routine to find the minimum expval
    n_wires = max(max(e) for e in edges) + 1
    depth = 4
    cost_h = build_cost_hamiltonian(edges, n_wires)
    dev = qp.device("default.qubit", wires=n_wires)

    @qp.qnode(dev)
    def cost_function(params):
        for w in range(n_wires):
            qp.Hadamard(wires=w)
        for layer in range(depth):
            qaoa_layer(params[0][layer], params[1][layer], edges, n_wires)
        return qp.expval(cost_h)

    params = np.array([[0.5] * depth, [0.5] * depth], requires_grad=True)
    optimizer = qp.GradientDescentOptimizer(stepsize=0.01)
    for _ in range(500):
        params = optimizer.step(cost_function, params)

    min_expval = float(cost_function(params))
    true_min = classical_min_energy(edges, n_wires)

    # Return the approximation ratio
    return float(min_expval / true_min)

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    ins = json.loads(test_case_input)
    output = approximation_ratio(ins)

    return str(output)

def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, rtol=5e-2
    ), "Your code does not yield the right approximation ratio"

# These are the public test cases
test_cases = [
    ('[[0, 1], [1, 2], [0, 2], [2, 3]]', '0.58160924'),
    ('[[0, 1], [1, 2], [2, 3], [3, 0]]', '0.94746734')
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
