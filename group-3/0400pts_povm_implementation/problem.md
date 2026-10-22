# Implementing POVMs  (400 pts)

- **Group:** Group 3
- **Status:** PASSED (submitted 2026-10-22 00:01:53 UTC)
- **Hidden test cases:** yes

---

## Challenge Statement

In introductory courses on quantum theory, we quickly get acquainted with the concept of a projective measurement. To get on the same page, let's quickly review the topic. 

When we measure an observable $B$ acting on a quantum system $S$, the possible outcomes are its eigenstates $\{\vert b_0\rangle, \vert b_1\rangle, \ldots, \vert b_N\rangle \},$  which form an orthonormal basis of the Hilbert space that represents $S$. Bohr's rule postulates that the probability of observing the eigenstate $\vert b_i \rangle$ when the quantum system is in the state $\vert \psi \rangle$ is 

$$ 
p(i) = \vert \langle b_i \vert \psi \rangle \vert^2.
$$

Alternatively, defining $P_i = \vert b_i\rangle\langle b_i \vert$, we can express

$$ 
p(i) = \langle \psi \vert P_i \vert \psi \rangle.
$$

Note that the operators $P_i$ are orthogonal projections, that is, they are Hermitian operators that satisfy 

- $P_i^2 = P_i,$
- $P_i P_j = 0$ when $i \neq j,$
- $\sum_{i=0}^{N}P_i = \mathbb{I}.$

We can model this type of measurement on $S$ by specifying the set $\{P_i\}$ of projectors. This set is known as a *projection-valued measure.*

In more advanced courses in quantum theory, we learn that there are more general measurements we can perform, some of which can be modelled through a *positive operator-valued measure,* or POVM for short. Generalizing the above, the measurement is specified via a set $\{E_i\}_{i=0}^{N}$ of positive hermitian operators such that

$$
\sum_{i=0}^{N}{E_i} = \mathbb{I}.
$$

The probabilities associated to the $i$-th measurement outcome are given by

$$ p(i) = \langle \psi \vert E_i \vert \psi \rangle.$$

In this challenge, we will construct a protocol that implements the measurement given by the POVM

$$
\begin{align*}
E_0 & = \alpha \vert 1 \rangle \langle 1 \vert, \\
E_1 & = \beta \vert - \rangle \langle - \vert, \\
E_2 & = \mathbb{I}-E_0 - E_1,
\end{align*}
$$

on one qubit. Here, $\alpha$ and $\beta$ are real numbers between $0$ and $1$. 

The protocol consists of coupling the qubit to an auxiliary qubit, evolving the two-qubit joint system, and finally measuring the joint system in the computational basis, as shown in the figure below. 

<p align="center">
<img src="https://s3.us-east-1.amazonaws.com/swc-prod-event-content-qhack-2026/challenge-images/povm_implementation/povm.png" width="400"/>
</p>

Denoting the probability of measuring the basis state $\vert i\rangle\vert j \rangle$ by $p_{ij}$ and the initial state of the qubit by $\vert \psi \rangle,$ the circuit should be such that

$$
\begin{align*}
p_{00} &= \langle \psi \vert E_0 \vert \psi \rangle, \\
p_{01} &= \langle \psi \vert E_1 \vert \psi \rangle, \\
p_{10} + p_{11} &= \langle \psi \vert E_2 \vert \psi \rangle.
\end{align*}
$$

Can you find the unitary that accomplishes this?

## Challenge code

In the code template shown, you must complete the circuit `implement_POVM`, which applies the unitary that implements the `alpha` and `beta`-dependent POVM. In `implement_POVM`, wire `0` must be the auxiliary qubit and wire `1` must be the system qubit.

You are also given some space to code any helper functions you may need. 
### Input

As input to this problem, you are given:

- `alpha` (`float`): Coefficient between $0$ and $1$ associated with the POVM element $E_0$
- `beta` (`float`): Coefficient between $0$ and $1$ associated with the POVM element $E_1$

### Output

Your circuit will be fed into a quantum device that measures the probabilities in the computational basis. This is done through the function `povm_circuit`, which is given for you in the challenge code.
Then, it will be run with ten random quantum states in order to verify that the output probabilities match the POVM probabilities. If they all match, the output will be `"Correct circuit"`. The relative error tolerance in the probabilities is `1e-4`.

### Test cases

The following **public test cases** are available to you. Note that there are additional **hidden test cases** that we use to verify that your code is valid in full generality.

```python
test_input: 0.25, 0.25
expected_output: "Correct circuit"

test_input: 0.2, 0.4
expected_output: "Correct circuit"
```

Good luck!


