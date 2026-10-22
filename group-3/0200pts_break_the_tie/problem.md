# Break the Tie  (200 pts)

- **Group:** Group 3
- **Status:** PASSED (submitted 2026-10-22 00:01:50 UTC)
- **Hidden test cases:** yes

---

You have a discrete random variable $X$ for which outcome $i$ occurs with probability $p_i$, and a non-negative quantity $f(X)$ defined on its outcomes. You want its average/expectation value,

$$
\mathbb{E}[f(X)] = \sum_i p_i \, f_i .
$$

Classically, we can estimate this by sampling: draw $N$ outcomes, evaluate $f$ on each, and average. Amplitude estimation performs the same task with an error that falls quadratically faster in the number of times the circuit is applied. That quadratic improvement is one of the attractive characteristics of quantum Monte Carlo. Part of the price for it is that the answer comes back ambiguous, and this challenge is about that ambiguity.


## Putting an average into an amplitude

In quantum Monte Carlo, there are two important steps. First, a unitary $\mathcal{A}$ loads the distribution onto $m$ data wires so that the squared amplitudes reproduce the probabilities:

$$
\mathcal{A} \lvert 0 \rangle^{\otimes m} = \sum_i \sqrt{p_i} \, \lvert i \rangle .
$$

Second, we add one objective wire, and a unitary $\mathcal{R}$ rotates it controlled on the data wires, so that the outcome $\lvert i \rangle$ puts amplitude $\sqrt{\tilde{f}_i}$ on $\lvert 1 \rangle$:

$$
\sum_i \sqrt{p_i} \, \lvert i \rangle \Big( \sqrt{1 - \tilde{f}_i} \, \lvert 0 \rangle + \sqrt{\tilde{f}_i} \, \lvert 1 \rangle \Big) .
$$

Amplitudes cannot exceed a value of $1$, so $f$ has to be rescaled into the $[0, 1]$ interval first. Dividing by $f_{\max} = \max_i f_i$ achieves this, giving $\tilde{f}_i = f_i / f_{\max}$.

If we then read the objective wire, we get

$$
\Pr[1] \; = \; \sum_i p_i \tilde{f}_i \; = \; \frac{\mathbb{E}[f(X)]}{f_{\max}} \; \equiv \; a .
$$

The desired average is now encoded in a single probability amplitude, and multiplication by $f_{\max}$ at the end recovers it.

## Why two answers come back

Amplitude estimation runs phase estimation on a Grover-like operator $\mathcal{Q}$ built from that state. $\mathcal{Q}$ acts as a rotation inside a two-dimensional invariant subspace, and a rotation has a conjugate pair of eigenvalues $e^{\pm 2 \pi i \theta}$. The circuit above prepares an *equal* superposition of the two corresponding eigenvectors. These have equal overlap, and therefore equal peak height.

With $n$ estimation wires the register reports a phase $\theta = k / 2^n$ for an integer bin $k$, from which

$$
a = \frac{1 - \cos(\pi \theta)}{2} .
$$

Because both eigenvectors are present in equal measure, the register shows two peaks of exactly equal height: one at bin $k$, one at bin $2^n - k$. The mirror bin corresponds to the phase $1 - \theta$, and $\cos(\pi(1 - \theta)) = -\cos(\pi\theta)$, so the two bins map to

$$
\frac{1 - \cos(\pi \theta)}{2} \quad \text{and} \quad \frac{1 + \cos(\pi \theta)}{2} ,
$$

which are $a$ and $1 - a$. Both are perfectly consistent with everything the algorithm measured. No amount of extra estimation wires will separate them, because sharpening the peaks sharpens both, so the ambiguity is structural to the algorithm rather than a matter of resolution.

It is worth having the relation in the forward direction as well, so that you can predict your own readout before running anything:

$$
\theta = \frac{\arccos(1 - 2a)}{\pi} , \qquad k = \mathrm{round}\!\left( 2^{n} \theta \right) .
$$

### A warning about the template's documentation

The worked example in the `qp.QuantumMonteCarlo` docstring resolves the ambiguity silently, with

```python
phase_estimated = np.argmax(circuit()[:int(N / 2)]) / N
```

The slice searches only the lower half of the estimation register, which amounts to always taking the smaller of the two candidates. That is right for the example it appears in but wrong in general. Note that following this procedure will fail on three of this challenge's test cases (one of which is public)

The same docstring also gives the relation twice: as $\mu = (1 + \cos(\pi\theta))/2$ in its algorithm summary, and as $\mu = (1 - \cos(\pi\theta))/2$ in its example. Those are not a typo. They are the two candidates, and which one applies depends on information the estimation register does not contain. Supplying that information is the work this challenge is asking for.

## Breaking the tie

Resolving the ambiguity requires information from outside the estimation. Any independent estimate of $a$ will do, provided it is accurate to better than half the distance between the two candidates. The candidates are $a$ and $1 - a$, so that distance is $\lvert 1 - 2a \rvert$ and the requirement is an error below $\lvert 0.5 - a \rvert$. The estimate does not need to be precise, only unambiguous. In this challenge's test cases the two candidates are between $0.13$ and $0.81$ apart.

As $a$ approaches $0.5$ the two candidates merge. That edge case is also why the mirror bin is taken modulo $2^n$: at $a = 0$ the peak sits at $k = 0$, which is its own mirror.

There is a method that allows you to readily perform this estimate: build the encoding directly on $m + 1$ wires and measure the objective wire. That gives $a$ outright, with no estimation register at all.

If that seems like cheating (if you can measure $a$ directly, why estimate it?), note what is actually being traded. Both circuits contain the same encoding, one controlled rotation per outcome, $2^m$ of them. The direct circuit applies it once and reads $\Pr[1]$, which is ordinary sampling and so costs $1/\varepsilon^2$ shots to reach accuracy $\varepsilon$. Amplitude estimation applies that same encoding inside $\mathcal{Q}$ roughly $2^n$ times, in one deep circuit, and reaches $1/\varepsilon$. Shots are traded for depth, not gates. The direct circuit is the cheap, shallow, coarse instrument you use to point the sharp one in the right direction, and the number you report at the end is the estimated one.

One thing this challenge deliberately does not exercise: the tests run on an exact simulator with no shots, so there is no sampling noise anywhere in it. The gap between your estimate and the true average comes purely from discretisation, because $2^n \theta$ has to be rounded to an integer bin. That is why the tolerance can be as tight as $10^{-9}$, and why reporting $\sum_i p_i f_i$ instead of the estimate would fail.

## Symbols

The names below follow the `qp.QuantumMonteCarlo` documentation, so that the challenge and the docs can be read side by side.

- $m$ -- data wires; the distribution has $2^m$ entries.
- objective wire -- one further wire, the last of `target_wires`, carrying $\sqrt{\tilde{f}_i}$.
- `target_wires` -- the $m$ data wires and the objective wire together, $m + 1$ in all. This is the single easiest argument to get wrong.
- $n$ -- estimation wires, which hold the phase readout.
- $N$ -- applications of $\mathcal{Q}$, or classical samples: the currency in which the two methods are compared.
- $\varepsilon$ -- absolute error on $\mathbb{E}[f(X)]$. The matching error on $a$ is $\delta = \varepsilon / f_{\max}$.
- $a$ -- the amplitude, equal to $\mathbb{E}[f(X)] / f_{\max}$.
- $\mathcal{A}$, $\mathcal{R}$, $\mathcal{Q}$ -- load the distribution, rotate the objective wire, and the Grover-like operator built from the two.

Two differences from the docstring are worth noting here:
- It calls the estimated quantity $\mu$, which is exactly this challenge's $a$. 
- Its $f$ is already rescaled into $[0, 1]$, so it is this challenge's $\tilde{f}_i$ and not the raw `values`. $f_{\max}$ has to be divided out before the function is handed to the template.

## Challenge code

Write

```python
estimate_mean(probabilities, values, n)
```


Your solution builds and runs two circuits, which you define first and then run using the `run_circuit(num_wires, circuit)` helper function:

The amplitude-estimation circuit, on $m + 1 + n$ wires. Call `qp.QuantumMonteCarlo` with `target_wires=range(m + 1)` (the $m$ data wires plus the objective wire) and the $n$ estimation wires after them, and measure the estimation register. This is the circuit that produces the two-peak readout, so it is where the two candidates come from. It cannot say which of them is correct.

The tie-breaker circuit, on $m + 1$ wires. Build the same encoding by hand: `qp.StatePrep` for the distribution on the data wires, then one multi-controlled `qp.RY` per outcome, and measure the objective wire. This gives $a$ outright, with no estimation register involved. That number is what tells you which candidate to keep, but it is not the number you report.


The Challenge Template gives you two helpers and you have to write the two circuit bodies described above. `rotation_angle(fraction)` is the angle that puts amplitude $\sqrt{\text{fraction}}$ on $\lvert 1 \rangle$. `run_circuit(num_wires, circuit)` builds an analytic simulator of `num_wires` wires, turns your circuit function into a QNode, runs it, and hands back the measurement as a list of floats.


### Inputs

Your function is called with three arguments:

- `probabilities` -- a `list` of `float`, the probability of each outcome. They sum to $1$, and the length is a power of two: length 8 means $m = 3$ data wires.
- `values` -- a `list` of `float`, all non-negative, the value of the quantity at each outcome. Same length as `probabilities`.
- `n` -- an `int`, the number of estimation wires.

Note that $m$ is not passed in. You derive it from the length of `probabilities`, with `m = int(round(np.log2(len(probabilities))))`.

A concrete call, which is the second public test case:

```python
estimate_mean([0.125] * 8,
              [0.6, 0.7, 0.8, 0.9, 1.0, 1.0, 1.0, 1.0],
              8)
```

Here `len(probabilities) == 8`, so $m = 3$. Your circuits therefore need $m = 3$ data wires, $1$ objective wire and $n = 8$ estimation wires. 12 wires for the estimation, and 4 for the direct encoding.

### Outputs

Return a single `float`: the estimated average of the quantity. It is $f_{\max}$ times whichever of the two candidate amplitudes your direct encoding identifies as the right one.

For the call above, the correct return is

```python
0.8745681972617296
```

Because this is the *estimate*, it will not agree exactly with $\sum_i p_i f_i$, which is $0.875$ here. The graded value is checked to an absolute tolerance of $10^{-9}$, so returning the exact average instead of the estimate fails.


### Rules

Within the two circuits the layout is free. The order of the data wires does not matter, the objective wire may sit before them rather than after, and any loading route works as long as the squared amplitudes are the probabilities, so `qp.MottonenStatePreparation` is accepted in place of `qp.StatePrep`.

### Checking your pipeline by hand

Every stage of the second public test case can be checked with a calculator, before any circuit runs. The distribution is uniform on 8 outcomes and the quantity sits close to its maximum of $1$, so $a = \mathbb{E}[f(X)]$ exactly:

```
f_max                                  1.0
a = E[f] / f_max                       0.875
theta = arccos(1 - 2a) / pi            0.769947
2**n * theta,  n = 8                 197.106
tallest bin k = round(2**n * theta)  197
mirror bin 2**n - k                   59
the two candidates                     0.125432  and  0.874568
reported mean, f_max * the right one   0.874568
exact sum(p_i f_i), for comparison     0.875
```

The register can only report the integer $197$, not $197.106$. That rounding is the entire difference between $0.874568$ and $0.875$: the estimate is not noisy, it is quantised. Both of those peaks are $0.4817$ tall, and between them they hold $96\%$ of the probability in the register.

### Public test cases

- input: `[[0.4008104395612045, 0.24310382032676792, 0.14744992052145606, 0.0894328975684541, 0.054243794362206846, 0.03290052437982574, 0.019955176756987287, 0.012103426523097706], [0.0, 0.25, 1.0, 2.25, 4.0, 6.25, 9.0, 12.25], 8]`
  expected output: `1.160949660702857`

- input: `[[0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125], [0.6, 0.7, 0.8, 0.9, 1.0, 1.0, 1.0, 1.0], 8]`
  expected output: `0.8745681972617296`

The first case is a decaying distribution and a squared quantity, and the answer is the smaller candidate. The second is the one traced above, where the answer is the larger. There is no way to tell which from the readout alone. Note that the recipe in the template's own documentation would return $0.125432$ for the second case.

