import json
import pennylane as qp
import pennylane.numpy as np

# Write any helper functions you need here

n_qubits = 4

dev = qp.device('default.qubit', wires = n_qubits)

@qp.qnode(dev)
def iqp_circuit(weights, pattern, observable):

    """This quantum circuit implements the IQP circuit with the given weight, pattern, and observable
    Args:
        weights (np.array(float)): The parameters of the IQP circuit.
        pattern (float): The pattern of the rotation groups as per challenge description.
        observable (np.array(int)): The array describing the observable as per challenge description

    Returns:
        (numpy.array): The expectation value of the observable for the prepared IQP state.
    """
    

    # Each group j shares the angle weights[j]; every subset S in that group
    # gets the rotation exp(-i * weights[j] / 2 * X_S)
    for j, group in enumerate(pattern):
        for subset in group:
            qp.PauliRot(weights[j], "X" * len(subset), wires=list(subset))

    # Build Z_a = product of Z_k over the wires where observable[k] == 1
    obs = None
    for k, a_k in enumerate(observable):
        if a_k == 1:
            obs = qp.PauliZ(k) if obs is None else obs @ qp.PauliZ(k)
    if obs is None:
        obs = qp.Identity(0)

    # Return the expectation value
    return qp.expval(obs)

def optimize_iqp(pattern, observable):

    """This function finds the weights that optimize the IQP circuit built above
    Args:
        pattern (float): The pattern of the rotation groups as per challenge description.
        observable (np.array(int)): The array describing the observable as per challenge description

    Returns:
        (numpy.array): The expectation value of the observable for the prepared IQP state.
    """

    # Initialize the weights
    def cost(w):
        return iqp_circuit(w, pattern, observable)

    np.random.seed(42)
    best_weights, best_cost = None, np.inf

    # Build an optimizer
    for _ in range(10):
        weights = np.array(np.random.uniform(-np.pi, np.pi, len(pattern)), requires_grad=True)
        opt = qp.AdamOptimizer(stepsize=0.1)
        for _ in range(300):
            weights = opt.step(cost, weights)
        current = float(cost(weights))
        if current < best_cost:
            best_cost, best_weights = current, weights
        if best_cost < -0.9999:
            break

    # Return the optimizing weights
    return np.array(best_weights)

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:

    test_pattern = json.loads(test_case_input)[0]
    test_observable = json.loads(test_case_input)[1]
    params = optimize_iqp(test_pattern, test_observable)
    cost = iqp_circuit(params, test_pattern, test_observable)
    weights = [0.3, -0.7, 0.2, 1.1]
    expval = iqp_circuit(weights, test_pattern, test_observable)
    out = [float(expval), float(cost)]
    return str(out)


def check(solution_output: str, expected_output: str) -> None:
    solution_expval = json.loads(solution_output)[0]
    expected_expval= json.loads(expected_output)[0]
    solution_min = json.loads(solution_output)[1]
    expected_min= json.loads(expected_output)[1]

    params = [0.3, -0.7, 0.2, 1.1]
    test_pattern = [[[0], [1]], [[1, 2]], [[0, 2], [1, 3]], [[0, 1, 2, 3]]]
    test_observable = [1, 0, 1, 0]
    names = list(qp.specs(iqp_circuit)(params, test_pattern, test_observable)['resources'].gate_types.keys())
    assert names.count('IQP') == 0, "You are not allowed to use PennyLane's built in IQP template"
    
    assert np.allclose(
        solution_expval, expected_expval, atol=1e-3
    ), "Your circuit doesn't look quite right "

    assert np.allclose(
        solution_min, expected_min, atol=2e-2
    ), "Your parameters don't look quite right "

# These are the public test cases
test_cases = [
    ('[[[[0], [1]], [[1, 2]], [[0, 2], [1, 3]], [[0, 1, 2, 3]]], [1, 0, 1, 0]]', '[0.7306816499355087, -1]'),
    ('[[[[0], [2]], [[1, 2, 3]], [[0, 1], [2, 3]], [[0, 1, 2]]], [1, 1, 0 ,1]]', '[0.9362933635841989, -1]')
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
