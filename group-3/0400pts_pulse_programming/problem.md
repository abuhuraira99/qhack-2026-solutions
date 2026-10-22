# Pulse Optimization  (400 pts)

- **Group:** Group 3
- **Status:** PASSED (submitted 2026-10-22 00:02:01 UTC)
- **Hidden test cases:** yes

---

## Challenge statement

Pulse programming is used as a method of controlling quantum operations in quantum systems. Essentially, a time-dependent electromagnetic field is applied to the quantum degrees of freedom, the state of whom are governed by time-dependent Schrödinger equation:

$$
\frac{\partial}{\partial t} \vert \psi \rangle = -i H(t) \vert \psi \rangle,
$$

where $H$ is the Hamiltonian that describes the system interacting with its environment. 

In this challenge, we're going to give you a Hamiltonian with tunable parameters (akin to tuning the electromagnetic field) and ask *you* to turn the knobs, let a quantum state evolve for some time, and generate a desired output state. You'll want to have the [documentation for `qp.pulse`](https://docs.pennylane.ai/en/stable/code/qml_pulse.html) handy if you're not familiar with it already!

Ok, so here's the deal. You're in the lab with a one-qubit pulse-programmable quantum computer. The Hamiltonian governing your system is this:

$$
H(t) = p_0t X + p_1t^2 Y + p_2t^3 Z,
$$

where $t = 2$ — this is hard-coded — and $p_i$ are tunable parameters. Your job is to evolve the $\vert 0 \rangle$ state for the given time and obtain a given target state, $\vert \psi \rangle$:

$$
\exp(-iH(t)t) \vert 0 \rangle = \vert \psi \rangle.
$$

To do this, you have to turn some knobs and figure out what the optimal values of $p_i$ are by maximizing the fidelity between $\vert \psi \rangle$ and $\exp(-iH(t)t) \vert 0 \rangle$ (or, equivalently, minimizing the *negative* of the fidelity) with respect to the parameters $p_i$:

$$
F = \vert \langle \psi \vert \exp(-iH(t)t) \vert 0 \rangle \ \vert^2.
$$

The maximum value of $F$ is $1$.

## Challenge code

In the code below you must complete the following functions:

1. `hamiltonian`: this function creates the time-dependent Hamiltonian provided in the description above. Create it similarly to what's outlined in the [`qp.pulse` documentation](https://docs.pennylane.ai/en/stable/code/qml_pulse.html).
2. `circuit`: this is a QNode that will only have one operation: an instance of `qp.evolve` that requires the Hamiltonian from the `hamiltonian` function. This QNode returns `qp.state()`.
3. `cost`: this function takes the output of `circuit` and `target_state` and calculates the fidelity. Check out the [`qp.math.fidelity_statevector` function in PennyLane's documentation](https://docs.pennylane.ai/en/stable/code/api/pennylane.math.fidelity_statevector.html).

### Input

As input to this challenge, you are given the target state (`list(float)`) that `circuit` must produce.

### Output

Your code will output the parameters $p_i$ (`list(float)`) such that $\exp(-iH(t)t) \vert 0 \rangle = \vert \psi \rangle$.

### Test cases

The following **public test cases** are available to you. Note that there are additional **hidden test cases** that we use to verify that your code is valid in full generality.

```python
test_input: [0.11775969, 0.99304212]
expected_output: [0.0, 0.062368193925808904, 0.0]
test_input: [0.7071067812, 0.7071067812]
sample_output:, [0.0, 0.26666667860250887, 0.0], 
```

Your `circuit` QNode must *only* contain 1 operation (an instance of `qp.evolve`). If your solution matches the correct one within the `1e-4` relative error tolerance, the output will be `"Success!"`. Otherwise, you will receive an `"Incorrect"` prompt.

Good luck!


