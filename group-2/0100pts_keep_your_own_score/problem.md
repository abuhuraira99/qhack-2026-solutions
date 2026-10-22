# Keep your Own Score  (100 pts)

- **Group:** Group 2
- **Status:** PASSED (submitted 2026-10-21 21:26:43 UTC)
- **Hidden test cases:** yes

---

A quantum computer does not measure observables. It measures qubits, and every qubit it measures comes back as a zero or a one. Everything else -- every expectation value, every energy, every correlator you have ever read off a quantum device -- is arithmetic performed afterwards on those bits.

This challenge asks you to do that arithmetic yourself, with no `qp.expval` anywhere.

## One qubit at a time

A measurement in the computational basis answers the question "is this qubit $\lvert 0 \rangle$ or $\lvert 1 \rangle$?", which is the same as measuring the observable $Z$, whose eigenvalues are $+1$ and $-1$:

$$
Z \lvert 0 \rangle = + \lvert 0 \rangle, \qquad Z \lvert 1 \rangle = - \lvert 1 \rangle .
$$

To measure $X$ or $Y$ instead, you do not need different hardware. You need a gate that carries the eigenvectors of $X$ or $Y$ onto the eigenvectors of $Z$, applied just before the measurement. The Hadamard gate does it for $X$, because $H X H = Z$:

$$
H \lvert + \rangle = \lvert 0 \rangle, \qquad H \lvert - \rangle = \lvert 1 \rangle .
$$

For $Y$ you first rotate $Y$ onto $X$ with the adjoint of the phase gate $S$, then apply a Hadamard. The pair $H S^{\dagger}$ satisfies $H S^{\dagger} Y S H = Z$, so applying $S^{\dagger}$ and then $H$ sends the eigenvectors of $Y$ to $\lvert 0 \rangle$ and $\lvert 1 \rangle$.

The pattern is worth stating plainly. A single-qubit Pauli measurement is a basis change followed by the only measurement the machine actually has.

## Many qubits at once

Now take a Pauli word such as $Z_0 \otimes Y_1 \otimes X_2$. Apply the basis change appropriate to each wire, and the word becomes $Z_0 \otimes Z_1 \otimes Z_2$. A single shot then produces three bits, and the value of the word on that shot is the product of the corresponding eigenvalues -- that is, $+1$ if an even number of the three bits came back as $1$, and $-1$ if an odd number did. This is a parity.

Averaging over shots, or reading the exact probabilities from a simulator, gives

$$
\langle P \rangle = \sum_{b} \; s_b \; p_b ,
$$

where $b$ runs over the eight computational-basis outcomes, $p_b$ is the probability of outcome $b$, and $s_b = \pm 1$ is that outcome's parity.

Two details decide whether your signs are right.

A wire carrying an identity factor is **not** part of the parity. The word $Z_0 \otimes I_1 \otimes Z_2$ does not care what wire 1 does, so wire 1's bit is skipped when counting -- which is not the same as forcing it to zero.

A wire carrying $Z$ **is** part of the parity even though it needs no basis change. The gate you apply and the wires you include in the parity are two independent decisions, and conflating them is the usual way this goes wrong.

## Challenge code

A three-qubit state is prepared for you by the `prepare` function in the Context section, which takes four angles. Write

```python
measure_pauli_word(word, angles)
```

which measures a Pauli word on that state using computational-basis probabilities only.

### Inputs

The test input is a Python list `[word, angles]`:

- `word` is a string of exactly three characters, each one of `"I"`, `"X"`, `"Y"` or `"Z"`. Character `w` is the Pauli factor acting on wire `w`, so `"ZIY"` means $Z$ on wire 0, identity on wire 1 and $Y$ on wire 2.
- `angles` is a list of four floats, to be passed straight to `prepare`.

The whole thing is four steps with only one circuit being executed. Your solution should: 

1. Translate the letters: EAch letter has exactly one basis change: `"I"` and `"Z"` need `"none"`, `"X"` needs `"H"`, `"Y"` needs `"SH"`.
2. Construct a circuit that prepares the state first, then loop over your `basis` list applyging the gates it names, and finally return the outcome probabilities.
3. Determine the signs: Outcome index `b` runs from `0` to `7` and is a three-bit number with wire 0 as the most significant bit. The bit on wire `w` is
```python
(b >> (2 - w)) & 1
```
For example `b = 5` is `101`, so wire 0 holds `1`, wire 1 holds `0` and wire 2 holds `1`. Count how many of those bits equal `1`, **looking only at the wires whose letter is not `"I"`**, and the sign is `-1` raised to that count -- an even count gives `+1`. Building the list of wires that participate first, with something like `[w for w, letter in enumerate(word) if letter != "I"]`, keeps step 3 short.
4. Determine the expectation value of the Pauli word.

### Outputs

Return a tuple of three items, in this order.

1. `basis`: a list of three strings, one per wire, recording the basis change you applied there. Use `"none"` for no gate, `"H"` for a single `qp.Hadamard(w)`, and `"SH"` for `qp.adjoint(qp.S(w))` followed by `qp.Hadamard(w)`.
2. `signs`: a list of eight integers, each `+1` or `-1`, giving the parity of each computational-basis outcome. Entry `b` corresponds to the outcome whose bit string is `b` written in binary with three digits, most significant bit on wire 0 -- the same ordering `qp.probs(wires=[0, 1, 2])` uses.
3. `value`: a float, the expectation value of the word, obtained as the sum over outcomes of probability times sign.

For the identity word `"III"` there is no basis change on any wire, every parity is `+1`, and the value is `1.0`.

### Rules

Build your device with `qp.device("default.qubit", wires=3)` and have your circuit return `qp.probs(wires=[0, 1, 2])`. Note that any other measurement is refused (`qp.expval`, `qp.state`, `qp.density_matrix` and friends) because the whole point is to get there from outcome probabilities.


### Test cases

Both cases use `prepare` exactly as given; only the word and the angles change.

- input: `["ZIZ", [0.79, 2.75, 2.89, 0.33]]`
  expected output: `[["none", "none", "none"], [1, -1, 1, -1, -1, 1, -1, 1], 0.931986472711103]`

- input: `["XYI", [1.45, 0.22, 1.72, 1.4]]`
  expected output: `[["H", "SH", "none"], [1, 1, -1, -1, -1, -1, 1, 1], 0.9673999542626387]`

The first case is worth reading closely. All three basis entries are `"none"`, because $Z$ needs no gate -- but the signs are not all `+1`, because wires 0 and 2 do enter the parity. Wire 1 carries the identity, so its bit is ignored: outcomes $000$ and $010$ both have sign $+1$.

Worked example for the word `"XYI"`: step 1 gives `["H", "SH", "none"]`; the wires that participate in the parity are 0 and 1; outcome `b = 0` is `000` so no bits are set and the sign is `+1`; outcome `b = 2` is `010`, which sets wire 1, one participating bit, so the sign is `-1`; outcome `b = 6` is `110`, which sets wires 0 and 1, two participating bits, so the sign is `+1` again. Wire 2 never affects a sign, because its letter is `"I"`.

Expectation values are checked to an absolute tolerance of $10^{-6}$. The basis and sign lists must match exactly.

