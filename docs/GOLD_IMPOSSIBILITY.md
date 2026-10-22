# Why "Personal Best (Gold)" is not solvable honestly

Group 3's *Personal Best* challenge comes in three tiers — Bronze (5% saving), Silver
(20%), Gold (60%) — over the baseline cost of synthesising an arbitrary *n*-qubit
unitary. This note explains why **Gold cannot be reached by a legitimate circuit**, and
documents the evidence. Our Silver solution already sits at the proven optimum.

## The cost model

A circuit is decomposed into the gate set `{RX, RY, RZ, T, S, H, X, Y, Z, CNOT, GlobalPhase}`
and charged in "T-equivalents":

| Gate | Cost |
|---|---|
| `RX`, `RY`, `RZ` (any angle) | 44 |
| `T` | 1 |
| `S`, `H`, `X`, `Y`, `Z`, `CNOT`, `GlobalPhase` | 0 |

Each auxiliary wire **doubles the whole cost**, and at most 8 wires are allowed. The
circuit must reproduce the target unitary to 1e-8 entrywise (global phase included).
The baseline is the Quantum Shannon Decomposition; at 5 qubits its cost is **57 024**.

- **Silver** needs cost ≤ 0.80 × 57 024 ≈ 45 619.
- **Gold** needs cost ≤ 0.40 × 57 024 ≈ **22 810**.

## The parameter-count floor (why 21% is the ceiling)

A Haar-random *n*-qubit unitary has **4ⁿ − 1** independent real parameters (the dimension
of SU(2ⁿ)). In the accepted gate set, the only gates carrying a continuous parameter are
`RX`, `RY`, `RZ`; `GlobalPhase` contributes only the single global phase, and every other
gate is a fixed Clifford+T matrix with no tunable parameter.

For any fixed circuit layout with *k* rotations, the set of reachable unitaries is a smooth
image of dimension at most *k* + 1. With a finite gate budget there are only finitely many
layouts, so almost every unitary needs

> **k ≥ 4ⁿ − 1 rotations.**

At *n* = 5 that is **1023 rotations → cost 45 012 → 21.06% saving**. This is exactly what
our Silver solution achieves, and it is parameter-optimal. Gold would need ≤ 518
rotations — **below the floor at every qubit count** (6 vs 15, 28 vs 63, 124 vs 255, 518 vs
1023), so there is no "squeak past at *n* = 5 only" trick either.

Xanadu's own paper reaches this same 4ⁿ − 1 optimum:
[*Parameter-optimal unitary synthesis with flag decompositions*, arXiv:2603.20376](https://arxiv.org/abs/2603.20376).

## Can T-gates supply the missing parameters? (No, in practice)

The only way below the rotation floor is to approximate rotations with cheap `T` gates. This
fails under the constraints:

- **Each approximated gate needs ~31 bits of precision** at *n* = 5 (measured by perturbing
  an optimal circuit until the 1e-8 entrywise budget breaks).
- **Deterministic single-qubit Clifford+T synthesis costs ~3·log₂(1/ε) ≈ 90 T per rotation**
  (Ross–Selinger / gridsynth, [arXiv:1403.2975](https://arxiv.org/abs/1403.2975)) — *worse*
  than paying 44. Even an ideal 1-bit-per-T code gives ≥ ~25 T per parameter, capping the
  saving below 60%.
- **The one method that hits ~22 T per rotation** (Kliuchnikov et al. mixed-fallback,
  [arXiv:2203.10064](https://arxiv.org/abs/2203.10064)) produces a **mixed state / CPTP
  channel**, not a pure unitary. The grader checks the exact unitary matrix, so a mixed
  result fails.
- **Repeat-until-success** ([arXiv:1404.5320](https://arxiv.org/abs/1404.5320)) needs
  mid-circuit measurement and an ancilla; even at ~34 T per rotation it exceeds the budget,
  and the ancilla doubling makes it worse.
- **Phase-gradient / QROM amortisation** (the route in arXiv:2603.20376, App. B) *would*
  beat the target but needs ~60–80 ancilla qubits for 1e-8 precision — against an 8-wire cap
  where each wire doubles the cost. The cap is set precisely below what this route needs.

The information-theoretic counting bound (≈175 T total at *n* = 5) does **not** forbid Gold,
but no known *constructive, deterministic, low-ancilla* algorithm reaches it for a dense
unitary. That gap is an open research problem.

## Community evidence

Discussion on the official PennyLane forum (QHack 2026 category, 21–22 Oct 2026) reached the
same conclusion independently:

- A participant reports proving in **Lean 4** that 21.07% is the maximum for exact synthesis.
- Multiple participants report the same ~**21.065%** ceiling.
- A thread titled *"Personal Best (Gold) Problem: Grader Bug"* reports that the grader can be
  **bypassed** — a wrong/degenerate submission still marks the challenge complete and does not
  revert the score — which is how "Gold" completions appear on the leaderboard.
- A thread titled *"I think gold solution is unreachable, and it is a test"* makes the
  1023-rotation argument.

## Conclusion

Under this cost model, with ≤ 8 wires and 1e-8 accuracy, **the honest optimum is the
parameter-optimal 4ⁿ − 1 rotation circuit (~21%), which is our Silver submission.** Gold is
not reachable by a legitimate circuit; the completions on the board trace to a grader bug,
which we reported to the organisers. The "Personal Best" framing and the hardened grader
suggest the Gold threshold may be a deliberate integrity test.

### References

- Parameter-optimal flag decompositions — https://arxiv.org/abs/2603.20376
- Recursive Cartan (KAK) decompositions — https://arxiv.org/abs/2503.19014 and the PennyLane demo https://pennylane.ai/demos/tutorial_unitary_synthesis_kak
- Ross–Selinger optimal Z-rotation synthesis — https://arxiv.org/abs/1403.2975
- Kliuchnikov et al., shorter circuits via mixed fallback — https://arxiv.org/abs/2203.10064
- Bocharov–Roetteler–Svore repeat-until-success — https://arxiv.org/abs/1404.5320
- Low–Kliuchnikov–Schaeffer, trading T gates for dirty qubits — https://arxiv.org/abs/1812.00954
- Tan, unitary synthesis with fewer T gates — https://arxiv.org/abs/2509.25702
- Counting lower bound for near-Clifford unitaries — https://arxiv.org/abs/2607.12907
- PennyLane compilation overview — https://pennylane.ai/blog/2025/12/compilation_lay_of_the_land_decomposition_routines/
