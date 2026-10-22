# Personal Best (Silver)  (200 pts)

- **Group:** Group 3
- **Status:** PASSED (submitted 2026-10-22 00:09:17 UTC)
- **Hidden test cases:** yes

---

Quantum algorithms are typically written in terms of unitary operators, such as a time evolution term, an oracle, or a block encoding. A quantum computer has no native gate for them in general, so before an algorithm can run, every such unitary has to be broken down into gates the hardware can actually execute. That step is unitary synthesis, and how good a synthesis is depends on what it costs.

A fault-tolerant quantum computer typically implements a Clifford+T gate set, where the T gate is the most expensive resource. An arbitrary rotation has no exact Clifford+T decomposition at all, so it has to be approximated by a sequence of T gates. Rotations are therefore expensive parts of the circuit, and the whole game is to use as few of them as possible. In this challenge every rotation costs the same, whatever its angle, and the circuit only has to meet a fixed accuracy, so the savings come from the structure of the circuit.

This challenge is about building an efficient unitary synthesis method. Your circuit is decomposed into the gate set below with `qp.decompose` to obtain their cost in terms of T-gates or their equivalent:

| Gate | Cost |
| --- | --- |
| `RX`, `RY`, `RZ`, any angle | 44 |
| `T` | 1 |
| `X`, `Y`, `Z`, `S`, `H`, `CNOT`, `GlobalPhase` | 0 |

The 44 is the expected T count for approximating one arbitrary rotation to a precision of $\epsilon = 10^{-9}$ with repeat-until-success circuits, from the "Simulation Results" section of Bocharov, Roetteler and Svore, [Efficient Synthesis of Universal Repeat-Until-Success Circuits](https://arxiv.org/abs/1404.5320):

$$
T_{\mathrm{count}} \approx 1.149 \log_{2}\left(\frac{1}{\epsilon}\right) + 9.2 \approx 43.6 .
$$

Anything outside that gate set is decomposed before it is counted.

Qubits are charged as well. Logical qubits are a scarce resource on an early fault-tolerant machine, so every wire you use beyond the $n$ data wires doubles your entire cost:

$$
C = \left( 44 \, N_{\mathrm{rot}} + N_{T} \right) \cdot 2^{\, N_{\mathrm{aux}}}
$$

A wire counts as soon as any gate in the decomposed circuit touches it, even if it is returned to $\lvert 0 \rangle$ afterwards. Your circuit may also use at most 8 wires in total. Every sample has to be simulated inside the challenge platform's time limit, and on your own machine if you test locally, so a circuit on more than 8 wires is rejected without being simulated.

The number to beat is the cost of the Shannon decomposition of Shende, Bullock and Markov (2006), which recurses on a cosine-sine split and spends

$$
C_{\mathrm{base}}(n) = 44 \left( \frac{21}{16} 4^{n} - 3 \cdot 2^{\,n-1} \right) ,
$$

or 13728 at four qubits.

Your challenge, should you choose to accept it, is to develop a unitary synthesis algorithm that requires fewer quantum resources than the Shannon decomposition! It is tested on unitaries of 2, 3, 4 and 5 qubits, so it has to work at every size, and its saving has to hold up as the size grows.

A valid circuit that saves less than 20% gets no grade. **This version of the challenge asks for Silver.** A higher grade also passes.

## Challenge code

Complete the function `submission_circ` which takes a Haar-random unitary `u_mat` and queues a circuit that implements it on wires `0` to `n - 1`.

Your solution must:

1. Implement `u_mat`, global phase included, to `1e-8` in absolute entrywise error with no relative tolerance.
2. Work for any unitary on 2, 3, 4 and 5 qubits. Assume no structure in `u_mat` at all.
3. Have a mean cost at or under the baseline $C_{\mathrm{base}}(n)$ at every size.
4. Have a saving against the baseline that never shrinks from one size to the next.
5. Save at least **20%** against the baseline at 5 qubits. This is what the Silver challenge asks for.

Rule 4 deserves a word. A saving that comes from the structure of your construction carries over to every new qubit, while a saving from removing a fixed number of gates fades as the circuit grows. In terms of cost, from one size to the next your cost may grow by at most the baseline's factor:

$$
\frac{C(n)}{C(n-1)} \le \frac{C_{\mathrm{base}}(n)}{C_{\mathrm{base}}(n-1)}.
$$

Important notes:

- PennyLane's default decompositions are not always the cheapest ones under this cost model. For example, `qp.adjoint(qp.T)` is decomposed into a rotation and costs 44, although $T^\dagger = T S Z$ exactly, which costs 1. Use `compile_circuit` to see what is actually counted.
- Auxiliary wires are allowed, up to 8 wires in total. They start in $\lvert 0 \rangle$ and must be returned to $\lvert 0 \rangle$, and each one doubles your cost. The grader enforces the return: it keeps only the part of the output in which every auxiliary wire is back in $\lvert 0 \rangle$, so a wire left in any other state shows up as an accuracy failure.
- The whole test has to run inside the challenge platform's time limit, so two practical limits apply. The decomposed circuit may hold at most 100,000 gates; the Shannon decomposition needs about 2300 at five qubits, so this only stops circuits that would take too long to simulate. And `submission_circ` itself is called once per sample, so keep its classical work to seconds: an exact construction does not need a numerical search.
- A hint to get started: `qp.QubitUnitary(u_mat, wires=range(n))` costs 660, 3212, 13948 and 57948, so it is just over the baseline from 3 qubits on. At 4 qubits the gap is five rotations. Find them first!

You do not need to change anything in the template. These helpers are there for you:

- `cost_of`: the grader's own cost, auxiliary-wire penalty included.
- `compile_circuit`: the decomposed circuit that is actually charged.
- `circuit_matrix`: the matrix your circuit implements on the data wires.
- `baseline_cost` and `haar_unitary`: the baseline and a random sample.
- `cs_decomposition` and `diagonalize_unitary`: the linear algebra (cosine-sine decomposition and unitary eigendecomposition), so you can spend your time on the circuit and not on LAPACK.

### Input

A Python `list` of two integers, `[seed, num_samples]`:

- `seed` (`int`): the seed the graded Haar-random samples are drawn from.
- `num_samples` (`int`): how many samples are drawn at each size in `TEST_SIZES`.

### Output

`submission_circ` returns `None`. The gates it queues are the answer, and the harness measures them for you. It reports one line per test case, for example:

```
{"grade": "Bronze", "saving_at_5_qubits": "14.5%", "next_grade": "Silver needs 20%", "saving_by_size": ["0.0%", "12.5%", "14.4%", "14.5%"], "cost": [660, 2772, 11748, 48708], "baseline": [660, 3168, 13728, 57024], "max_error": "1.2e-12", "aux_wires": 0}
```

If your circuit is not valid or saves less than 20%, `grade` is `"None"` and a `reason` tells you which rule failed. The example above is valid and reaches Bronze, so it does not pass this Silver version.

The expected output of every test case is the grade this version asks for, for example `{"required_grade": "Silver"}`.

### Test cases

The following public test cases are available to you. Note that there are additional hidden test cases that we use to verify that your code is valid in full generality. All cases differ only in the seed and the number of samples, so a solution that works on the public cases and fails on the private ones is a solution that has been fitted to particular matrices.

**Case 1.** Input `[2026, 2]`. Two samples at each of 2, 3, 4 and 5 qubits, eight unitaries in all. The reference Shannon decomposition, with every fixed phase spelled as a Clifford gate, gives:

```
{"grade": "None", "reason": "Valid, but below Bronze: it saves 0.0% against the baseline at 5 qubits.", "saving_at_5_qubits": "0.0%", "next_grade": "Bronze needs 5%", "saving_by_size": ["0.0%", "0.0%", "0.0%", "0.0%"], "cost": [660, 3168, 13728, 57024], "baseline": [660, 3168, 13728, 57024], "max_error": "1.4e-12", "aux_wires": 0}
```

It sits exactly on the baseline at every size, so it is valid (a saving that stays at 0% does not shrink), but it saves nothing and gets no grade. It is the starting point: every grade asks you to beat it.

**Case 2.** Input `[7, 2]`. The same thing on a different seed.

Good luck!

