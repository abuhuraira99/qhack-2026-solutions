# The Scouting Report  (100 pts)

- **Group:** Group 2
- **Status:** PASSED (submitted 2026-10-19 18:08:41 UTC)
- **Hidden test cases:** yes

---

When we use PennyLane as a quantum circuit simulator, we can cheat and ask for `qp.state()` and the full state vector comes back, amplitudes and all. On hardware that function does not exist. All you ever get back are the expectation values of observables you chose to measure, and if you did not choose to measure something, that information is simply gone.

So how do you learn what a qubit *is*, using only expectation values?

Any single-qubit state is completely determined by three real numbers. This can be represented in the Pauli basis as follows :

$$
\rho = \frac{1}{2} \left( I + r_x X + r_y Y + r_z Z \right), \qquad r_i = \mathrm{Tr}\left( \rho \, \sigma_i \right) = \langle \sigma_i \rangle .
$$

Where $\sigma_{i} = \{I, X, Y, Z\}$. The coefficients $\left( r_x, r_y, r_z \right)$ are the Bloch vector. The second equality (where $\mathrm{Tr(A)}$ is the trace of matrix $A$) is the crux of this coding challenge: each component of the Bloch vector *is* an expectation value that we can estimate by measuring three observables. That is single-qubit state tomography, the smallest instance of a ubiquitous technique in quantum information experiments.

We can also define a quantity known as the purity, which gives a measure of the length of the Bloch vector, as:

$$
\mathrm{Tr}\left( \rho^2 \right) = \frac{1}{2} \left( 1 + r_x^2 + r_y^2 + r_z^2 \right) ,
$$

such a unit-length Bloch vector means a pure state, and a vector of length zero means the maximally mixed state $I/2$, with purity $1/2$. Everything in between is known as a partially mixed state.


Suppose the qubit you are characterising is one half of a two-qubit circuit, and you ignore the other half. Then a purity below 1 is representative of entanglement with the qubit you are not measuring. For a Bell state, the reduced state of either qubit is exactly $I/2$: the Bloch vector is the zero vector and the purity is $1/2$, the minimum possible. The state of the pair is perfectly pure and perfectly known, yet neither qubit individually has any state at all. All of the information lies in the correlations, and looking at one wire in isolation cannot see it.


## Challenge code

In the code below you must complete this function:

- `bloch_and_purity`: returns the Bloch vector and purity of one wire. Its arguments are:

    - `prep` (`callable`): a black-box state preparation acting on all wires. You may call it inside your circuits, but you may not inspect it.
    - `num_wires` (`int`): the total number of wires in the device.
    - `target_wire` (`int`): the wire to characterise.

You may use only `qp.expval`. Note that this is enforced: the grader records every measurement your circuits send to the device and rejects a submission that uses any measurement other than an expectation value. `qp.state`, `qp.density_matrix`, `qp.probs` and `qp.purity` all read the simulator's state directly, which no hardware can do, so all four are refused. Build your circuits on the `dev` provided for you rather than a device of your own, or the grader will see no measurements at all and reject that too.

Note that `target_wire` is genuinely an argument. It is not always wire 0, and the register is not always two wires wide, so measure the wire you are given rather than the wire the example happens to use.

### Input

A `dict` with two keys:

- `"gates"`: a `list` of gate specifications describing the state preparation. Each entry is a `[gate_name, parameters, wires]` triple, in which `gate_name` is a `str` naming a PennyLane operation, `parameters` is a `list` of `float` and is empty for a gate that takes none, and `wires` is a `list` of `int`.
- `"target_wire"`: an `int`, the wire to characterise.

For example:

```
{"gates": [["Hadamard", [], [0]], ["CNOT", [], [0, 1]]], "target_wire": 1}
```

The test harness applies the gates in order to build the `prep` callable that your function receives, infers `num_wires` from the largest wire index used, and passes `"target_wire"` straight through as `target_wire`. You never handle this dictionary yourself.

### Output

A `tuple` of two objects: a `list` of three `float`, the Bloch components `[r_x, r_y, r_z]`, followed by a `float`, the purity. All four numbers must match to within an absolute numerical tolerance of `1e-5`.

Good luck!

