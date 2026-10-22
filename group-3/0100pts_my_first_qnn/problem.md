# My First Quantum Neural Network  (100 pts)

- **Group:** Group 3
- **Status:** PASSED (submitted 2026-10-22 00:00:51 UTC)
- **Hidden test cases:** yes

---

One of the primary focuses of PennyLane is quantum machine learning, in which quantum neural networks play a key role. In this coding challenge, we will construct the building blocks of a quantum neural network—the encoding block $\mathcal{S}(x)$ and the trainable block $\mathcal{A}(\vec{\theta})$:

<p align="center">
<img src="https://s3.us-east-1.amazonaws.com/swc-prod-event-content-qhack-2026/challenge-images/my_first_qnn/description_a_s.png" width="400"/>
</p>

When applied sequentially, they will constitute one layer of the quantum neural network. In this challenge, your task is to build the following single-qubit, single-layer quantum model (and perform a measurement at the end):

<p align="center">
<img src="https://s3.us-east-1.amazonaws.com/swc-prod-event-content-qhack-2026/challenge-images/my_first_qnn/s_a.png" width="400"/>
</p>

---
**NOTE**: After measurement, classical optimization is applied to update the trainable parameters $\vec{\theta}$ and potentially enable the model to learn how to solve classification or regression problems. However, this goes beyond the scope of this particular challenge.

---

## Challenge code

In the code template shown, you must complete the following quantum functions:

- `encoding_circuit`: A quantum function that applies the $\mathcal{S(x)}$ operator and returns nothing. The arguments of this function are:

    - `x` (`float`): variable that we want to encode in our quantum circuit.

- `training_circuit`: A quantum function that applies the $\mathcal{A(\vec{\theta})}$ operator and returns nothing. The arguments of this function are:

    - `theta_vec` (`np.ndarray(float)`): An array [theta_1, theta_2, theta_3] of angle parameters for the RZ, RY and RZ gates, respectively.

Then, you must complete the main function `quantum_neural_network` that combines both `encoding_circuit` and `training_circuit`:

- `quantum_neural_network`: A QNode that applies the functions `encoding_circuit` and the `training_circuit` and returns the expectation value $\langle\hat{\sigma}^z\rangle$. The arguments of this function are:

    - `x` (`float`): Variable that we want to encode in our quantum circuit.
    - `theta_vec` (`np.ndarray(float)`): An array [theta_1, theta_2, theta_3] of angle parameters for the RZ, RY and RZ gates, respectively.

### Input

As an input to this problem, you are given the variable $x$ as a `float` and the array $\vec{\theta}$  as an `np.ndarray(float)`.

### Output

The code must output an `np.tensor` that corresponds to the expectation value of the circuit `quantum_neural_network`.

### Test cases

The test cases are given as arrays of the form $[x, \vec{\theta}]$. The following **public test cases** are available for you to check your work. There are also some **hidden test cases**, which we will use to check that your solution works in full generality.

```python
test_input: [0.4859371, 1.32682562, -1.06015833, -4.41959946]
expected_output: 0.827549
test_input: [-0.72318627, -4.91395046, -5.0609724, 0.1125593]
expected_output: 0.865457
```

If your solution matches the correct one within the given tolerance specified in check (in this case it's a 1e-4 relative error tolerance), the output will be `"Success!"`. Otherwise, you will receive an `"Incorrect"` prompt.

All the best!


