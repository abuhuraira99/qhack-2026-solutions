# Playing Period  (100 pts)

- **Group:** Group 1
- **Status:** PASSED (submitted 2026-10-19 15:45:06 UTC)
- **Hidden test cases:** yes

---

## Challenge Statement

The Quantum Fourier Transform (QFT) is one of the most important subroutines in quantum computing. It is used in the most famous algorithms such quantum phase estimation and Shor's factoring algorithm!

For a system of $n$ qubits, the QFT transforms a computational basis state $|x\rangle$ according to

$$
|x\rangle
\longrightarrow
\frac{1}{\sqrt{2^n}}
\sum_{y=0}^{2^n-1}
e^{2\pi ixy/2^n}|y\rangle.
$$

This transformation exists in PennyLane, but in this challenge you are going to build it from elementary gates, namely
Hadamard gates (`qp.Hadamard`), controlled phase rotations (`qp.ControlledPhaseShift`), and SWAP gates (`qp.SWAP`). We will focus on the four qubit QFT. 

## Challenge Code

Complete the function `qft_four_qubits` to implement the Quantum Fourier Transform on wires `[0,1,2,3]` using only the following PennyLane operations: `qp.Hadamard`, `qp.ControlledPhaseShift`, and `qp.SWAP`.

You may NOT use `qp.QFT` in your solution.

Remember that the standard QFT circuit naturally produces the qubits in reversed order. Your circuit should include the appropriate SWAP gates so that its output agrees with PennyLane's implementation for the QFT.

The function does not need to return anything. It should simply apply the required gates to the circuit.

### Input

There are no inputs to this challenge. 
 
### Output

There are no outputs in this challenge. The grader will compare your circuit  with `qp.QFT` to check that the outputs are the same.

### Test cases

There are no test cases, since there are no input or outputs.

Good luck!


