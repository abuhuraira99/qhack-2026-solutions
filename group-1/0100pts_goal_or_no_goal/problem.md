# Goal or No Goal?  (100 pts)

- **Group:** Group 1
- **Status:** PASSED (submitted 2026-10-19 15:42:08 UTC)
- **Hidden test cases:** yes

---

A GHZ state is the many-qubit generalization of a Bell pair:

$$
|\mathrm{GHZ}_n\rangle = \frac{1}{\sqrt{2}} \left( |00\ldots0\rangle + |11\ldots1\rangle \right).
$$

A natural next question is how you would *prove* you actually built one, on hardware, where all you ever get back are the expectation values of observables you chose to measure (and not the exact state, like you can do with simulators).

One obvious first attempt is to measure every qubit in the computational basis and look at the histogram of bitstrings. For the GHZ state you get only two of them, all-zeros and all-ones, each with probability $1/2$, and every other bitstring should never appear. But that is not sufficient.

Consider a machine that flips a fair coin and, depending on the result, prepares either $|00\ldots0\rangle$ or $|11\ldots1\rangle$. That state can be described by the matrix: 

$$
\rho_{\mathrm{mix}} = \frac{1}{2} |00\ldots0\rangle\langle 00\ldots0| + \frac{1}{2} |11\ldots1\rangle\langle 11\ldots1| .
$$

This machine produces exactly the same $Z$-basis sampling histogram as a GHZ state. No number of computational-basis shots will ever separate the two, because the difference between them lives entirely in the off-diagonal terms of the matrix (known as the coherences, which characterize the relationship between states) and $Z$ basis measurements are blind to these coherences.

Separating these two cases requires an observable that is sensitive to the off-diagonal terms (the coherences). The measure that sees the coherences is the global $X$-basis parity, described by,

$$
\Pi_X = X_0 X_1 \cdots X_{n-1} .
$$

A parity observable is a product of single-qubit Pauli operators, for example $Z_0 Z_1$ or $X_0 X_1 X_2$. Because each Pauli squares to the identity, such a product has only two eigenvalues, $+1$ and $-1$. Measuring it therefore asks a single yes-or-no question rather than reading out individual qubits. Specifically, the question it asks is one of evenness. The global $X$-basis parity reports whether the number of qubits found in $|-\rangle$ is even or odd.

$$
\langle \mathrm{GHZ}_n | \, \Pi_X \, | \mathrm{GHZ}_n \rangle = +1 , \qquad \mathrm{Tr}\left( \rho_{\mathrm{mix}} \, \Pi_X \right) = 0 .
$$

## One more catch

There is one more subtlety. The $X$ parity on its own also does not uniquely identify the GHZ state. Consider the completely unentangled product state $|+\rangle^{\otimes n}$. Every qubit is a $+1$ eigenstate of its own $X$, so

$$
\langle +|^{\otimes n} \, \Pi_X \, |+\rangle^{\otimes n} = +1
$$

for every $n$. This is a case where we have perfect $X$ parity, but no entanglement in the state so we could once again be led astray!

In other words, the $X$ parity is blind to the populations (the distribution of how often the system of qubits is in one state versus another) in exactly the way the $Z$ histogram is blind to the coherences (the measure of the relationship that exists between states).

Neither test is sufficient on its own, but together they are. We can write down a list of $n$ parity checks that the GHZ state passes and no other state does, as: 

$$
\Pi_X = X_0 X_1 \cdots X_{n-1}, \qquad Z_i Z_{i+1} \quad \text{for } i = 0, 1, \ldots, n-2 .
$$

The $n-1$ neighbouring $ZZ$ parities pin the populations onto all-zeros and all-ones; the single global $X$ parity certifies that those two branches are coherently superposed.

So the quantity to report is the mean of all $n$ checks:

$$
s_n = \frac{1}{n} \left( \langle \Pi_X \rangle + \sum_{i=0}^{n-2} \langle Z_i Z_{i+1} \rangle \right),
$$

which equals $+1$ if and only if the state is $|\mathrm{GHZ}_n\rangle$.


Other states that would have given us similar results of one of these measures do not satisfy this fuller test. For example:
- $|+\rangle^{\otimes n}$ scores $1/n$, 
- the classical mixture scores $(n-1)/n$, and 
- the wrong-phase state $\left( |00\ldots0\rangle - |11\ldots1\rangle \right)/\sqrt{2}$ scores $(n-2)/n$.


## Challenge code

Your task is to complete this function:

- `prepare_and_build_checks`: prepares the state and returns the checks to measure on it. Its argument is:

    - `n` (`int`): the number of qubits, guaranteed to be at least 2.

    It returns:

    - `checks` (`list`): the $n$ observables to measure. The order does not matter.

That function does two things: it applies the gates that prepare the GHZ state on the device wires, and it builds the list of $n$ observables to measure on that state. Everything around it is provided in the code provided for you and needs no changes. `wrapper(n)` creates the `n`-wire device and defines a QNode called `parities`, which calls your `prepare_and_build_checks(n)`, measures the expectation value of every observable in the list you return, and averages them into the score. Because your function is called from inside that QNode, every gate you apply there lands on the circuit, and every observable you return gets measured.

The grader inspects the observables you return, not just the number that comes out. It requires exactly $n$ of them, each a plain product of Pauli operators with coefficient $1$, and specifically the global $X$ parity together with the $n-1$ adjacent $Z_i Z_{i+1}$ pairs written above. Returning $n$ copies of the identity, or the same check $n$ times, scores nothing.

### Input

A single integer `n`, the number of qubits, for example `3`.

### Output

A `float`: the mean of the $n$ parity values, equal to `1.0` for a correctly prepared GHZ state. Your answer must match to within an absolute numerical tolerance of `1e-5`.

### Test cases

The following **public test cases** are available to you. Note that there are additional hidden test cases that we use to verify that your code is valid in full generality.

```python
test_input: 
n: 3
expected_output: 1.0

test_input: 
n: 5
expected_output: 1.0
```
The score is $1$ for every $n$, because it is an average of $n$ checks that a correct GHZ state passes perfectly. That makes the expected output uninformative on its own: what distinguishes a correct solution is which observables produced it, which is what the grader inspects. Floating-point arithmetic will leave you a little short of exactly $1$, which is why the tolerance is there.

Good luck!

