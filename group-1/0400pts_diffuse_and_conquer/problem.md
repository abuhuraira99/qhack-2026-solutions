# Diffuse and Conquer  (400 pts)

- **Group:** Group 1
- **Status:** PASSED (submitted 2026-10-19 17:14:37 UTC)
- **Hidden test cases:** yes

---

## Challenge Statement

A chemical species is suspended in a fluid. As time passes, the species diffuses through the fluid while undergoing a reaction that causes it to decay. 
The concentration $\phi(x,t)$ is governed by the one-dimensional diffusion-reaction equation

$$
\frac{\partial \phi}{\partial t}
=
\nu\frac{\partial^2\phi}{\partial x^2}
-k\phi+s(x,t),
$$

where $\nu$ is the diffusion coefficient, $k$ is the reaction rate, and $s(x,t)$ describes a source of the chemical species (reality is three-dimensional though, take this as a simplification for learning purposes!)

In this challenge, the diffusion coefficient $\nu$ and reaction rate $k$ will be given as inputs. Your goal is to use QSVT to determine the concentration profile after one time step.

In order to do this, we need to express the PDE in discrete terms. We discretize the fluid into four interior spatial points separated by

$$
h=0.2.
$$

The concentration field at a given time can therefore be represented by the vector

$$
\boldsymbol{\phi}
=
\begin{pmatrix}
\phi_1\\
\phi_2\\
\phi_3\\
\phi_4
\end{pmatrix},
$$

where $\phi_i$ is the concentration at the $i$-th spatial point.

Using a central finite-difference approximation, the second spatial derivative is represented by

$$
D_2=
\frac{1}{h^2}
\begin{pmatrix}
-2&1&0&0\\
1&-2&1&0\\
0&1&-2&1\\
0&0&1&-2
\end{pmatrix}.
$$

We evolve the system through a time step

$$
\Delta t=0.01
$$

using the backward Euler method. The diffusion–reaction equation can then be written as the linear system

$$
A\boldsymbol{\phi}_{\mathrm{new}}=\mathbf b,
$$

where

$$
A=(1+k\Delta t)I-\nu\Delta t D_2
$$

and

$$
\mathbf b=
\boldsymbol{\phi}_{\mathrm{old}}
+\Delta t\,\mathbf s.
$$

In this challenge, $h$, $\Delta t$, $\boldsymbol{\phi}_{\mathrm{old}}$, and $\mathbf s$ are fixed and provided in the starter code. Only $\nu$ and $k$ change between experiments.

Classically, we could obtain the new concentration simply by calculating

$$
\boldsymbol{\phi}_{\mathrm{new}}=A^{-1}\mathbf b.
$$

You, however, will use **Quantum Singular Value Transformation (QSVT)** to approximately implement this inverse.

## Challenge Code

Complete the function `qsvt_diffusion` that uses QSVT to approximate the solution to the next time step of the differential equation above. See figure below for reference

<p align="center">
<img src="https://s3.us-east-1.amazonaws.com/swc-prod-event-content-qhack-2026/challenge-images/diffuse_and_conquer/diffuse_and_conquer_1.png" width="400"/>
</p>

You will need to find some phase angles for QSVT that approximate the polynomial $C/x$, for some real number $C.$

Please put your `C` and `qsvt_angles` in your code, as they will be used by the grader. 

You have some free space for helper functions, use it wisely!

Your solution should:

1. Construct the matrix $A$ corresponding to the supplied values of $\nu$ and $k$.
2. Construct an appropriate polynomial approximation to the inverse $C/x$
3. Determine the QSVT phase angles corresponding to this polynomial and specify the value of $C$
4. Use QSVT to approximately apply the inverse of $A$.

The grader will use your value of $C$ to rescale your output for the QSVT circuit and compare with the true solution. The test cases should be lenient enough that reasonable QSVT phases should work, but please note that the grader is looking for fidelity > 0.99. Make sure to refine your angles properly if some test cases fail! 
 

### Input

As input to this problem, you are given a list containing the diffusion coefficient `nu` (`float`) and the reaction rate `k` (`float`).
 
### Output

This code will output a `np.array(float)` with the solution to the concentration vector after one time step. 

### Test cases

The following **public test cases** are available to you. Note that there are additional **hidden test cases** that we use to verify that your code is valid in full generality.

```python
test_input: [0.2,0.5]
expected_output: [0.27959746, 0.42869397, 0.56892447, 0.64371709]

test_input: [1.0, 1.2]
expected_output: [0.28550356, 0.4595721 , 0.59350887, 0.59584262]
```

If your solution matches the correct one within the given tolerance specified in `check` (in this case, it's a fidelity greater than 0.99 of the approximate solution with respect to the analytical solution), the output will be `"Success!"` Otherwise, you will receive an `"Incorrect"` prompt.

Good luck!


