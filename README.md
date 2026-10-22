# QHack 2026 — Quantum Coding Championship

My team's solutions and write-up for the QHack 2026 Quantum Coding Championship (October 16–23, 2026), built with [PennyLane](https://pennylane.ai).

**Team:** AbuHuraira's Team  ·  **Handle:** @abuhuraira

## Result

- **Challenges solved:** 22 / 23
- **Points:** 4800
- **Peak rank:** #2 of 1652 teams
- Every challenge our team submitted passed the public **and** hidden test cases on the first correct submission.

The three groups unlocked on a schedule; each was solved within minutes of unlocking.

## Challenges

### Group 1  (unlocked 2026-10-16 14:00 UTC)

| Challenge | Points | Status | Solution |
|---|---|---|---|
| Goal or No Goal? | 100 | ✅ Solved | [`goal_or_no_goal`](group-1/0100pts_goal_or_no_goal/) |
| Playing Period | 100 | ✅ Solved | [`playing_period`](group-1/0100pts_playing_period/) |
| The Draft Lottery | 200 | ✅ Solved | [`draft_lottery`](group-1/0200pts_draft_lottery/) |
| The Hidden Subgroup Stage | 200 | ✅ Solved | [`the_hidden_group_stage`](group-1/0200pts_the_hidden_group_stage/) |
| Fermionic VQE | 200 | ✅ Solved | [`vqe_fermionic`](group-1/0200pts_vqe_fermionic/) |
| Grover's Little Helper | 400 | ✅ Solved | [`auxiliary_grover`](group-1/0400pts_auxiliary_grover/) |
| Diffuse and Conquer | 400 | ✅ Solved | [`diffuse_and_conquer`](group-1/0400pts_diffuse_and_conquer/) |

### Group 2  (unlocked 2026-10-19 18:00 UTC)

| Challenge | Points | Status | Solution |
|---|---|---|---|
| Building a Quantum Kernel | 100 | ✅ Solved | [`building_quantum_kernel`](group-2/0100pts_building_quantum_kernel/) |
| Keep your Own Score | 100 | ✅ Solved | [`keep_your_own_score`](group-2/0100pts_keep_your_own_score/) |
| The Scouting Report | 100 | ✅ Solved | [`scouting_report`](group-2/0100pts_scouting_report/) |
| A Relay of Phases | 200 | ✅ Solved | [`a_relay_of_phases`](group-2/0200pts_a_relay_of_phases/) |
| Nuclear Magnetic Resonance | 200 | ✅ Solved | [`nuclear_magnetic_resonance`](group-2/0200pts_nuclear_magnetic_resonance/) |
| A Basket of Options | 400 | ✅ Solved | [`a_basket_of_options`](group-2/0400pts_a_basket_of_options/) |
| Approximation Ratio for QAOA | 400 | ✅ Solved | [`qaoa_approx_ratio`](group-2/0400pts_qaoa_approx_ratio/) |

### Group 3  (unlocked 2026-10-22 00:00 UTC)

| Challenge | Points | Status | Solution |
|---|---|---|---|
| My First Quantum Neural Network | 100 | ✅ Solved | [`my_first_qnn`](group-3/0100pts_my_first_qnn/) |
| Personal Best (Bronze) | 100 | ✅ Solved | [`personal_best_bronze`](group-3/0100pts_personal_best_bronze/) |
| Same Kit, Different Number | 100 | ✅ Solved | [`same_kit_diff_number`](group-3/0100pts_same_kit_diff_number/) |
| Break the Tie | 200 | ✅ Solved | [`break_the_tie`](group-3/0200pts_break_the_tie/) |
| Personal Best (Silver) | 200 | ✅ Solved | [`personal_best_silver`](group-3/0200pts_personal_best_silver/) |
| The Salary Cap | 200 | ✅ Solved | [`salary_cap`](group-3/0200pts_salary_cap/) |
| Personal Best (Gold) | 400 | ⚠️ Attempted | [`personal_best_gold`](group-3/0400pts_personal_best_gold/) |
| Implementing POVMs | 400 | ✅ Solved | [`povm_implementation`](group-3/0400pts_povm_implementation/) |
| Pulse Optimization | 400 | ✅ Solved | [`pulse_programming`](group-3/0400pts_pulse_programming/) |

## The Personal Best (Gold) challenge — why it is not solvable honestly

Group 3 included a three-tier unitary-synthesis challenge (Bronze/Silver/Gold). Our Silver solution is **parameter-optimal**: it implements an arbitrary *n*-qubit unitary with exactly 4ⁿ−1 rotations, the theoretical minimum, matching the optimum in Xanadu's own paper [*Parameter-optimal unitary synthesis with flag decompositions* (arXiv:2603.20376)](https://arxiv.org/abs/2603.20376).

The **Gold** tier asks for a 60% cost reduction, which is below the information-theoretic floor for this cost model. A full analysis, with citations and the community discussion, is in [`docs/GOLD_IMPOSSIBILITY.md`](docs/GOLD_IMPOSSIBILITY.md).

## Repository layout

```
group-1/ group-2/ group-3/   one folder per challenge: problem.md + solution.py
docs/                        write-ups (Gold impossibility analysis, results)
screenshots/                 dashboard, leaderboard and per-challenge screenshots
```

## Running a solution

Each `solution.py` is the complete challenge file (context + solution + public tests). With PennyLane 0.45.1:

```bash
python group-2/0100pts_building_quantum_kernel/solution.py
```

---

*Leaderboard snapshot taken 2026-10-22 01:14:14 UTC. The competition was still live when this repository was created, so it was kept private until the event closed.*