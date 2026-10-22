# Fermionic VQE  (200 pts)

- **Group:** Group 1
- **Status:** PASSED (submitted 2026-10-19 15:50:52 UTC)
- **Hidden test cases:** yes

---

The Variational Quantum Eigensolver (VQE) is a key algorithm for quantum chemistry on near-term quantum computers. The main idea behind it is to train a quantum computer to prepare the ground state of a given molecule by finding the minimum expectation value of the molecular Hamiltonian.

VQE starts with a molecular Hamiltonian and a parametrized circuit that prepares a candidate ground state for the molecule. Then, the cost function is defined as the expectation value of the Hamiltonian in this trial state. By iteratively minimizing this cost function, VQE finds the ground state of the target Hamiltonian, which corresponds to the minimum eigenvalue. Usually, the optimization is performed using a gradient descent method.

A particular area of interest where VQE finds application is molecular and spin systems. These kinds of systems can be described by Hamiltonians that feature the fermionic creation $\hat{a}^\dagger$ and annihilation $\hat{a}$ operators.

In PennyLane, these Hamiltonians can be implemented with the [Fermi module](https://docs.pennylane.ai/en/stable/code/qml_fermi.html) by using a *FermiWord*, which consists of a product of fermionic operators, and *FermiSentence*, which consists of a linear combination of Fermi words. 

In this challenge you will have to construct a Hamiltonian of this form:

$$
H=c_0\hat{a}_0\hat{a}_0^\dagger+c_1\hat{a}_1\hat{a}_1^\dagger+c_2\hat{a}_2\hat{a}_2^\dagger,
$$

where `coeffs`=$[c_0,c_1,c_2]$ is a list of coefficients that will be given to you as an input and the 6 fermionic operators will be mapped to 6 qubits. You can map this to a qubit Hamiltonian as a function of Pauli operators using [`qp.jordan_wigner`](https://docs.pennylane.ai/en/stable/code/api/pennylane.jordan_wigner.html).
Then, you are asked to provide a quantum circuit that implements the VQE circuit and a subroutine that optimizes the trainable parameters to prepare the ground state of the given Hamiltonian.

**NOTE**: The `qp.fermi.jordan_wigner` mapping returns the coefficients of the qubit Hamiltonian as complex numbers, even when the Hamiltonian is Hermitian and every imaginary part is zero. Make sure the Hamiltonian you build has real coefficients.


## Challenge code

In the code below, you must complete these functions:

- `build_hamiltonian`: A function that builds and returns the qubit Hamiltonian with the input coefficients. The arguments of this function are:

    - `coeffs` (`list(float)`): A list of coefficients that will multiply the Pauli words to form the Pauli sentence that will be used to build the Hamiltonian.

- `vqe_circuit`: A QNode which represents the VQE circuit and returns the trial ground state energy. The arguments of this function are:

    - `params`(`np.array`): An array with the trainable parameters of the Variational Quantum Eigensolver circuit.
    - `coeffs` (`list(float)`): A list of coefficients that will multiply the Pauli words to form the Pauli sentence that will be used to build the Hamiltonian.

- `optimization`: A function that optimizes the parameters of the VQE circuit and returns the final ground state energy. The arguments of this function are:

    - `coeffs` (`list(float)`): A list of coefficients that will multiply the Pauli words to form the Pauli sentence that will be used to build the Hamiltonian.

### Input 

The input of this problem is the list `coeffs` that you will need to build the Hamiltonian.

### Output

This code must output a `(np.tensor)` with the minimum eigenvalue of the Hamiltonian. 

### Test cases

The following **public test cases** are available for you to check your work. There are also some **hidden test cases** which we will use to check that your solution works in full generality.

```python
test_input = [-2,2,5]
expected_output = -2

test_input = [7,6,-6]
expected_output = -6
```

If your solution matches the correct one, the output will be `"Success!"`. Otherwise, you will receive an `"Incorrect"` prompt.

All the best!
