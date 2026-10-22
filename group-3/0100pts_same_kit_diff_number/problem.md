# Same Kit, Different Number  (100 pts)

- **Group:** Group 3
- **Status:** PASSED (submitted 2026-10-22 00:01:51 UTC)
- **Hidden test cases:** yes

---

Two different matrices can be the same gate.

If $V = e^{i\alpha} U$ for some real $\alpha$, then $U$ and $V$ act identically on every state, and no measurement performed on that qubit can tell them apart. The reason is that measurement probabilities are built from squared magnitudes: for any state $|\psi\rangle$ and any observable, the phase $e^{i\alpha}$ appears once in the amplitude and once, conjugated, in its complex conjugate, so it cancels:

$$
\left| \langle \phi | V | \psi \rangle \right|^2 = \left| e^{i\alpha} \right|^2 \left| \langle \phi | U | \psi \rangle \right|^2 = \left| \langle \phi | U | \psi \rangle \right|^2 .
$$

This is why $-H$ and $H$ are the same gate, and why `qp.matrix` returning a matrix that differs from yours by a sign may not be an error.

## Turning a global phase into a relative phase

A global phase multiplies the whole state, so it drops out in the measurement process. A relative phase between two branches of a superposition does not. This is effectively what gives rise to interference effects in the measurement process at the end of a quantum computation. Controlling a gate converts the former into the latter.

Suppose $M = e^{i\alpha} I$ and put the control wire in $|+\rangle$ with the target in $|0\rangle$. The controlled operation acts on the $|1\rangle$ branch only:

$$
\mathrm{ctrl}(M) \, \frac{|0\rangle + |1\rangle}{\sqrt{2}} \otimes |0\rangle = \frac{|0\rangle + e^{i\alpha} |1\rangle}{\sqrt{2}} \otimes |0\rangle .
$$

The target remains untouched, but the control now carries a relative phase $\alpha$. A second Hadamard turns that phase into an observable measure of population,

$$
H \, \frac{|0\rangle + e^{i\alpha}|1\rangle}{\sqrt{2}} = \cos\left(\frac{\alpha}{2}\right) e^{i\alpha/2} |0\rangle - i \sin\left(\frac{\alpha}{2}\right) e^{i\alpha/2} |1\rangle ,
$$

so the probability of reading $1$ on the control is

$$
P(1) = \sin^2\left( \frac{\alpha}{2} \right) .
$$

This is the mechanism behind phase kickback, and behind quantum algorithms that read an eigenvalue out of a controlled unitary.

## Challenge statement

You are handed two $2 \times 2$ unitaries, $U$ and $V$. You will need to construct the quantity

$$
M = V U^{\dagger} ,
$$

and answer the following three questions.

1. Is $V$ the same gate as $U$ up to a global phase? 
2. If so, what is that phase $\alpha$, folded into the range $[0, 2\pi)$? If not, report `0.0`.
3. Implement the phase kickback circuit described above with the control and target wires initialised as |0>. What is the probability of measuring 1 on the control wire?

$$
\text{control: } |0\rangle \longrightarrow H \longrightarrow \bullet \longrightarrow H \longrightarrow \text{measure}
$$

$$
\text{target: } |0\rangle \longrightarrow M
$$

## Challenge code

You must complete this function:

- `same_gate_and_phase`: returns the verdict, the phase, and the control probability. Its arguments are:

    - `u_matrix` (`np.ndarray`): a $2 \times 2$ complex unitary.
    - `v_matrix` (`np.ndarray`): a $2 \times 2$ complex unitary.

### Input

Each test case is a Python `dict` with two keys, `"u"` and `"v"`. Each matrix is written as a list of 2 rows, each row a list of 2 entries, and each entry a `[real, imaginary]` pair of floats. The second public test case, $U = X$ and $V = Z$, looks like this:

```
{
    "u": [[[0.0, 0.0], [1.0, 0.0]],
          [[1.0, 0.0], [0.0, 0.0]]],
    "v": [[[1.0, 0.0], [0.0, 0.0]],
          [[0.0, 0.0], [-1.0, 0.0]]],
}
```

You never handle that pair format yourself. The grading code converts both matrices into single complex `np.ndarray`s before calling your function, so `u_matrix` and `v_matrix` arrive as ordinary $2 \times 2$ arrays of complex numbers.

The two public test cases are $U = H$ with $V = -H$ (the same gate, with $\alpha = \pi$), and $U = X$ with $V = Z$ (not the same gate). The remaining cases are hidden.

### Output

Return a `tuple` of three plain Python values:

```
(same_gate, alpha, p_one)
```

- `same_gate` (`bool`): whether $V$ is $U$ up to a global phase.
- `alpha` (`float`): the phase in $[0, 2\pi)$, or `0.0` when `same_gate` is `False`.
- `p_one` (`float`): the probability of measuring $1$ on the control wire.

The two floats are compared to within a tolerance of `1e-5`.

Good luck!

