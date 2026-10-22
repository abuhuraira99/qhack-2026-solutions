# The Salary Cap  (200 pts)

- **Group:** Group 3
- **Status:** PASSED (submitted 2026-10-22 00:01:46 UTC)
- **Hidden test cases:** yes

---

Resource estimation is sometimes presented in the following (simplified) flow: pick a quantum algorithm (represented by a circuit of a certain size), compile it, count the T gates, multiply by a per-T-gate time (based on some assumptions), and read off a runtime:

$$
T_{\mathrm{wall}} = N_T \cdot t_T .
$$

It is often helpful to think of resource estimation in the following alternative direction: given certain characteristics of a quantum computer (e.g, a fixed logical T-gate time, fixed by the code distance and the cycle time, a given number of logical qubits available, and a timeline for the project or for allocated compute time), how large of a problem, represented by a given algorithm, fits within those constraints?

Quantum phase estimation is a good place to ask at a high level, because the trade-off is fairly clean. With $m$ estimation wires the phase resolution is

$$
\epsilon = 2^{-m} ,
$$

so every extra wire gets you exactly one more bit of the phase. It also costs you roughly a doubling of the work, because QPE applies the controlled base unitary $\sum_{k=0}^{m-1} 2^k = 2^m - 1$ times. One more bit for twice the runtime is part of the bargain of phase estimation, and it is a far better bargain than sampling, where one more decimal digit costs a factor of one hundred extra samples/shots.

With (textbook) quantum phase estimation, two characteristics decide the answer to the earlier question of how large of a problem we might be able to run given certain hardware constraints.

The first is the base unitary. The T-count of QPE depends directly on what you are estimating the phase of. If you use a single-qubit rotation, the powers $U^{2^k}$ collapse, for example $R_Z(\theta)^{2^k} = R_Z(2^k \theta)$, so the controlled-powers block does not grow at all, and the cost you measure is in larger part the cost of the inverse QFT. A generic multi-qubit unitary on the other hand has no such structure, its powers genuinely accumulate, and the controlled-powers block dominates.

The second is the rotation synthesis precision. There is no exact Clifford+T circuit for an arbitrary rotation, so every rotation must be approximated, at a cost that grows roughly like $\log(1/\epsilon_{\mathrm{rot}})$ T gates apiece.

A key characteristic of resource estimation is that it is a symbolic calculation. It never builds a state vector, so it will easily cost a routine on hundreds of qubits that could not be simulated on any classical computer.

## Challenge code

In the code below you must complete this function:

- `affordable_precision`: returns the largest QPE size that fits a wall-clock budget. Its arguments are:

    - `t_gate_seconds` (`float`): the time to execute one logical T gate, in seconds.
    - `budget_seconds` (`float`): the total wall-clock budget, in seconds.
    - `max_estimation_wires` (`int`): a safety bound on the search. A correct model never reaches it.

Take the base unitary to be a generic two-qubit unitary, `qre.QubitUnitary(num_wires=2)`, and build phase estimation on it with `qre.QPE`. Cost it in the gate set `GATE_SET` provided in the code, with the single-qubit rotation precision set to `ROTATION_PRECISION` through a `qre.ResourceConfig`.

The runtime of a size is its T-count times `t_gate_seconds`, and a size is affordable when that runtime is no greater than `budget_seconds`. You want the largest affordable `m`. Because the T-count grows monotonically in `m`, you may stop at the first size that overruns.

There are two rules on how the answer is reached, both enforced by tests:

- The T-count you return must match what `qre.estimate` reports at the size you return. Reading it out of the result object is the point of the exercise, rather than reproducing it from a formula worked out beforehand.
- Your search must cost more than one size. Finding the largest size that fits means comparing sizes, so `qre.estimate` has to be called at least twice. How you search is up to you. For example, a scan upwards from `m = 1` and a binary search both pass.

### Input

A Python `list` of two floats, `[t_gate_seconds, budget_seconds]`:

- `t_gate_seconds` (`float`): the time to execute one logical T gate, in seconds.
- `budget_seconds` (`float`): the total wall-clock budget, in seconds.

### Output

A Python `tuple` of three values, `(num_estimation_wires, precision, t_count)`:

- `num_estimation_wires` (`int`): the largest affordable `m`.
- `precision` (`float`): the phase resolution `2 ** -m` that size buys.
- `t_count` (`int`): the T-count at that size, as reported by `qre.estimate`.


The wire count and the T-count are compared exactly, so cast them with `int(...)`; the resolution is compared to a relative tolerance of `1e-12`, which any of `2.0 ** -m`, `0.5 ** m` or `1 / 2 ** m` will satisfy. Return plain Python numbers rather than NumPy scalars, a NumPy integer or boolean cannot be serialised by the grader.

### Test cases
Two test cases are shown to you; the remaining cases are hidden and run when you submit.

As an example, for input `[1e-06, 1.0]`, your solution should output `(9, 0.001953125, 684108)`.

This means that a logical T gate takes one microsecond and you have one second of machine time, so the budget is a million T gates. Walking up the sizes, `m = 9` costs 684,108 T gates, which is 0.684 seconds and fits, while `m = 10` costs 1,366,956 T gates, which is 1.367 seconds and does not. So nine wires is the largest affordable size, and it gets you a phase resolution of $2^{-9} = 0.001953125$.

Good luck!

