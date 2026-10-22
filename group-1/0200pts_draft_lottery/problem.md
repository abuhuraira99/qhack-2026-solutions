# The Draft Lottery  (200 pts)

- **Group:** Group 1
- **Status:** PASSED (submitted 2026-10-19 15:54:57 UTC)
- **Hidden test cases:** yes

---

Phase estimation is usually introduced with a promise attached: you are handed an eigenvector of the unitary operator you are using, and the algorithm hands back its eigenphase. That promise is almost never kept in practice. One rarely knows the eigenvectors of the operator you care about. If you did, you would already have its spectrum. What actually goes into the target register is some state that happens to overlap several eigenvectors at once.

The good news is that the algorithm still works, and it even does something more useful.

## Leveraging linearity

Let $U$ have eigenvectors $\lvert u_k \rangle$ with eigenphases $\theta_k$, so that $U \lvert u_k \rangle = e^{2 \pi i \theta_k} \lvert u_k \rangle$. Phase estimation with $m$ estimation wires acts as

$$
\lvert u_k \rangle \lvert 0 \rangle^{\otimes m} \; \longmapsto \; \lvert u_k \rangle \lvert \tilde{\theta}_k \rangle ,
$$

where $\lvert \tilde{\theta}_k \rangle$ is the estimation register holding the $m$-bit approximation of $\theta_k$. The circuit is linear, so feeding it a superposition feeds every branch through at once. Writing the target state as $\lvert \psi \rangle = \sum_k c_k \lvert u_k \rangle$:

$$
\lvert \psi \rangle \lvert 0 \rangle^{\otimes m} \; \longmapsto \; \sum_k c_k \lvert u_k \rangle \lvert \tilde{\theta}_k \rangle .
$$

Now measure only the estimation register. The target register is left alone, so the branches cannot interfere, and the probability of reading the bit string $\tilde{\theta}_k$ is given by

$$
\Pr[\tilde{\theta}_k] = \lvert c_k \rvert^2 .
$$

One run of the circuit therefore samples an eigenphase, with each eigenphase appearing in proportion to how much of it your input state contained. The estimation register's probability distribution is a picture of the spectrum, weighted by overlap. This is the mechanism behind quantum eigensolvers: prepare a state you hope resembles your state of interest, run phase estimation, and the eigenvalue/eigenphase of your state of interest shows up with probability equal to the squared overlap you managed to achieve.

Two consequences follow, and this challenge is about both.

**Reading the spectrum.** Bin $k$ of the estimation register corresponds to the phase $k / 2^m$. If you collect every bin with non-negligible probability, you have the eigenphases present, along with their weights. If two different eigenvectors share the same eigenphase, they land in the same bin and their weights add. Keep in mind the register measures phases, not eigenvectors, and cannot tell them apart.

**Paying for the faint ones.** An eigenphase with weight $w$ appears in a single run with probability $w$. That means that a weight of one percent is not a small inconvenience, it is a factor of a hundred extra shots in runtime. Specifically, to see such an eigenphase at least once with probability $99 \%$ you need $r$ independent repetitions, where

$$
(1 - w)^r \le 0.01 \qquad \Longrightarrow \qquad r \ge \frac{\ln 0.01}{\ln (1 - w)} ,
$$

rounded up. This is why overlap, not just circuit depth, is a critical characteristic in eigenvalue estimation and why a poor initial guess can be more expensive than a deeper circuit.

## Challenge code

Write

```python
read_spectrum(phases, amplitudes, m)
```

The Challenge Template gives you `unitary_matrix(phases)`, which builds a diagonal unitary whose eigenvalue on basis state $\lvert k \rangle$ is $e^{2 \pi i \, \theta_k}$. Because it is diagonal, its eigenvectors are the computational-basis states, which makes the weights easy to reason about but does not change anything about the algorithm.

Build a device with the target wires first and the $m$ estimation wires after them, prepare `amplitudes` on the target register, run phase estimation, and measure the estimation register.

### Inputs

Your function is called with three arguments:

- `phases` -- `list[float]`. One eigenphase in $[0, 1)$ per computational-basis state of the target register. `len(phases)` is a power of two, so `len(phases) == 2` means one target wire and `len(phases) == 4` means two.
- `amplitudes` -- `list[float]`. Real, normalised amplitudes for the target register, with `len(amplitudes) == len(phases)`. Entry `amplitudes[k]` sits on basis state $\lvert k \rangle$, so `amplitudes[k] ** 2` is the weight of eigenphase `phases[k]`. Pass this list straight to a state preparation.
- `m` -- `int`. The number of estimation wires.

So a call looks like this:

```python
read_spectrum([0.1875, 0.6875], [0.8, 0.6], 4)
```

which is one target wire holding $0.8 \lvert 0 \rangle + 0.6 \lvert 1 \rangle$, read with four estimation wires.

Every test case uses eigenphases that are exact multiples of $1 / 2^m$, so each one lands in a single bin and the peaks are sharp. You do not have to deal with spectral leakage here.

### Outputs

Return a plain Python tuple of three items, in this order:

```python
return eigenphases, weights, repetitions
```

- `eigenphases` -- `list[float]`. The distinct phases present, in ascending order. Keep a bin if its probability exceeds `1e-9`.
- `weights` -- `list[float]`. The total probability of each phase, in the same order, so that `weights[i]` belongs to `eigenphases[i]`.
- `repetitions` -- `int`. The number of independent runs needed to observe the faintest phase at least once with probability at least $99 \%$.

### Test cases

These two cases are public, and both are shown in full. The remaining cases are private, and run only when you submit.

```python
read_spectrum([0.1875, 0.6875], [0.8, 0.6], 4)
# -> ([0.1875, 0.6875], [0.6399999999999999, 0.3599999999999996], 11)

read_spectrum([0.125, 0.375, 0.625, 0.875], [0.7, 0.5, 0.5, 0.1], 3)
# -> ([0.125, 0.375, 0.625, 0.875], [0.4899999999999996, 0.2499999999999999, 0.25, 0.009999999999999993], 459)
```

The weights carry the usual floating-point noise -- `0.6399999999999999` is $0.64$, and `0.009999999999999993` is one percent -- so do not try to reproduce those digits. They are compared to a tolerance.

In the first case one target wire carries $0.8 \lvert 0 \rangle + 0.6 \lvert 1 \rangle$, so the two eigenphases arrive with weights $0.64$ and $0.36$; the faintest needs $11$ repetitions. The second case has four eigenphases, one of which holds only one percent of the state -- and that single faint phase drives the cost to $459$ repetitions, more than forty times the first case, on a shallower circuit.

Eigenphases are checked to an absolute tolerance of $10^{-9}$ and weights to $10^{-6}$. The repetition count must match exactly.

