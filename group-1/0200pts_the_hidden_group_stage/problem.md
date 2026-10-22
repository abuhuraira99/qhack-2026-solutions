# The Hidden Subgroup Stage  (200 pts)

- **Group:** Group 1
- **Status:** PASSED (submitted 2026-10-19 16:00:23 UTC)
- **Hidden test cases:** yes

---

## Challenge Statement

The Hidden Subgroup Problem (HSP) has applications in Quantum Machine Learning, since symmetries can reveal hidden structure in data. Let us see a simple application of the concepts in the HSP to a classification problem!

You are given data consisting for binary strings $
x\in\mathbb{F}_2^n $ 
together with class labels $f(x)$. We suspect that the labels may be invariant under an XOR transformation

$$
x\longrightarrow x\oplus s,
$$

where $s\neq 0$ is a candidate symmetry. What does it mean that it's a "symmetry of the data"? It means that

$$
f(x)=f(x\oplus s).
$$

Thus, $x$ and $x\oplus s$ are considered "equivalent" and should be assigned the same label.

In this challenge, you will to use a quantum circuit to determine how compatible the observed training data is with the candidate symmetry $s$.
Don't fret, in this challenge we will guide you a little on how to do this.

First, for each class label $r$, collect all training inputs with that label:

$$
X_r=\{x_i:f(x_i)=r\}.
$$

Encode those inputs in the state

$$
|X_r\rangle
=
\frac{1}{\sqrt{|X_r|}}
\sum_{x\in X_r}|x\rangle.
$$

You may assume that the training inputs are distinct.

Now apply Hadamard gates to every qubit:

$$
H^{\otimes n}|X_r\rangle.
$$

Recall (or be today years old when you learned) that

$$
H^{\otimes n}|x\rangle
=
\frac{1}{\sqrt{2^n}}
\sum_y(-1)^{x\cdot y}|y\rangle.
$$

If $X_r$ contains a complete pair

$$
\{x,x\oplus s\},
$$

it is possible to show that the only states that survive in the superposition are those belonging to the set

$$
H_s^\perp
=
\{y:y\cdot s=0\}.
$$

With this in mind, you can add one ancilla qubit initialized in $|0\rangle$.
For every string element position $j$ such that

$$
s_j=1,
$$

apply

```python
qp.CNOT(wires=[j, ancilla])
```

For this circuit, the probability of measuring the ancilla in $|0\rangle$ is

$$
p_r(s)=P(y\cdot s=0),
$$

which measures how strongly class $r$ respects the proposed symmetry.

Finally, combine the class probabilities using into the symmetry score

$$
S(s)
=
\sum_r
\frac{|X_r|}{N}p_r(s)
$$

where $N$ is the total number of training points.

A larger value of $S(s)$ means that the candidate symmetry is more compatible with the observed data.

## Challenge Code

Complete the `symmetry_score`  given in the template, which takes the `data`, its `labels`, and the candidate symmetry `s`. `s` is binary string(`np.arrays` or 0s and 1s). The `data` is an `np.array` containing binary strings that are of the same length as `s`. The `labels` array is the same length as `data`, and contains integers `int` that indicate the class that each element in the data belongs in. 

Your function should return the weighted score $S(s)$ (`float`), calculated with the prescription above. Note that this problem has an analytical solution and you could not implement the circuit if you don't want to, but that might be the harder way to go about this challenge! 

## An example

In case all of the above is too abstract (it is!), here is an example to clarify.

```python
data = np.array([
    [0, 0, 0],
    [1, 1, 0],

    [0, 0, 1],
    [1, 1, 1],

    [1, 0, 1],
])

labels = np.array([
    0, 0,
    1, 1,
    2
])

s = np.array([1, 1, 0])
```

The first class contains

$$
\{000,110\},
$$

while the second contains

$$
\{001,111\}.
$$

Both are complete pairs related by

$$
s=110.
$$

For these classes,

$$
p_0(s)=p_1(s)=1.
$$

The final class contains only one training point. A single computational basis state becomes uniformly distributed after the Hadamard transform, giving

$$
p_2(s)=\frac12.
$$

The score is therefore

$$
S(s)
=
\frac25(1)
+
\frac25(1)
+
\frac15\left(\frac12\right)
=
0.9.
$$

Hopefully this grounded things a little!
 

### Input

As input to this problem, you are given the `data`, its `labels`, and the candidate symmetry `s`, as described above.
 
### Output

This code will output a `float` corresponding to the symmetry score $S(s)$. 

### Test cases

The following **public test cases** are available to you. Note that there are additional **hidden test cases** that we use to verify that your code is valid in full generality.

```python
test_input: 
data: [[0, 0, 0], [1, 1, 0], [0, 0, 1], [1, 1, 1], [1, 0, 1]]
labels: [0, 0, 1, 1, 2]
s: [1,1,0]

expected_output: 0.9

test_input: 
data: [[0, 0, 0], [1, 1, 0], [0, 0, 1]]
labels: [0, 0, 0]
s: [1,1,0]

expected_output: 0.833333333333333
```

If your solution matches the correct one within the given tolerance specified in `check` (in this case, it's a `1e-3` absolute error tolerance), the output will be `"Success!"` Otherwise, you will receive an `"Incorrect"` prompt.

Good luck!


