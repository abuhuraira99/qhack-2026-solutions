import json
import pennylane as qp
import pennylane.numpy as np

# Define the Pauli words

w0 = qp.FermiWord({(0, 0): "-", (1, 0): "+"})
w1 = qp.FermiWord({(0, 1): "-", (1, 1): "+"})
w2 = qp.FermiWord({(0, 2): "-", (1, 2): "+"})

def build_hamiltonian(coeffs):
    """
   Build the Hamiltonian with the input coefficients.
    Args:
        coeffs (list(float)): A list of coefficients that will multiply the Pauli words to form the Pauli sentence that will be used to build the Hamiltonian.
    Returns: 
        An operator that corresponds with the desired Hamiltonian.
    """

    fermi_h = coeffs[0] * w0 + coeffs[1] * w1 + coeffs[2] * w2
    qubit_h = qp.jordan_wigner(fermi_h)
    c, ops = qubit_h.terms()
    return qp.Hamiltonian([float(np.real(x)) for x in c], ops)

dev = qp.device("default.qubit", wires=6)
@qp.qnode(dev)
def vqe_circuit(params,coeffs):
    """
    The quantum circuit of the VQE
    Args:
        params(np.array): An array with the trainable parameters of the Variational Quantum Eigensolver circuit.
        coeffs (list(float)): A list of coefficients that will multiply the Pauli words to form the Pauli sentence that will be used to build the Hamiltonian.
    Returns: 
        (np.tensor): A numpy tensor of 1 element corresponding to the expectation value of the cost Hamiltonian.
    """

    for i in range(3):
        qp.RY(params[i], wires=i)
    return qp.expval(build_hamiltonian(coeffs))

def optimization(coeffs):
    """
    A function to optimize the parameters of the VQE circuit.
    Args:
        coeffs (list(float)): A list of coefficients that will multiply the Pauli words to form the Pauli sentence that will be used to build the Hamiltonian.
    Returns: 
        (np.tensor): A numpy tensor of 1 element corresponding to the minimum eigenvalue of the Hamiltonian, i.e., the expectation value of the cost Hamiltonian
        with the parameters optimized.
    """

    params = np.array([np.pi / 2] * 3, requires_grad=True)
    opt = qp.AdamOptimizer(stepsize=0.1)
    for _ in range(200):
        params = opt.step(lambda p: vqe_circuit(p, coeffs), params)

    return vqe_circuit(params,coeffs)

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    coeffs = json.loads(test_case_input)
    np.random.seed(40)
    output = optimization(coeffs)
    return str(output)
def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert abs(solution_output - expected_output)< 0.1

# These are the public test cases
test_cases = [
    ('[-2,2,5]', '-2'),
    ('[7,6,-6]', '-6')
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
