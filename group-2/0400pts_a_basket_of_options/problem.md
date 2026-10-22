# A Basket of Options  (400 pts)

- **Group:** Group 2
- **Status:** PASSED (submitted 2026-10-19 18:16:01 UTC)
- **Hidden test cases:** yes

---

## Challenge Statement

Diversification is one of the fundamental ideas of finance: instead of investing in a single asset, investors hold portfolios containing many different assets. The value of such a portfolio depends not only on how each asset behaves individually, but also on how their prices move **together**.

In this challenge, we have two assets whose prices $S_1$ and $S_2$ following correlated geometric Brownian motions. Long story short, this means that, at a future time $T$, their prices can be written as

$$
S_{i,T}
=
S_{i,0}
\exp\left[
\left(r-\frac{\sigma_i^2}{2}\right)T
+\sigma_i\sqrt{T}Z_i
\right],
$$

where $r$ is the risk-free interest rate, $\sigma_i$ is the volatility of asset $i$, and the random variables $Z_1$ and $Z_2$ follow a correlated bivariate standard normal distribution,

$$
\begin{pmatrix}
Z_1\\
Z_2
\end{pmatrix}
\sim
\mathcal N
\left(
\begin{pmatrix}
0\\
0
\end{pmatrix},
\begin{pmatrix}
1 & \rho\\
\rho & 1
\end{pmatrix}
\right).
$$

Consider now a basket containing a fraction (between $0$ and $1$) $w$ of the first asset and $1-w$ of the second. Its value at time $T$ is

$$
B_T=wS_{1,T}+(1-w)S_{2,T}.
$$

A European call option is a contract that allows you (but does not obligate you) to pay a strike price $K$ for the basket at a maturity time $T$. An option written on this basket has payoff

$$
g(S_{1,T},S_{2,T})
=
\max(B_T-K,0).
$$

This means that at time $T,$ you make a profit is the value of the basket is greater than $K.$ Otherwise, you just don't pay $K$ for something that is actually cheaper, and have zero profit.

Some smart people (does the name Feynman ring a bell?) proved that the fair value of the option (you don't get the option for free!) can be calculated as

$$
V_0
=
e^{-rT}
\mathbb E\left[
\max\left(
wS_{1,T}+(1-w)S_{2,T}-K,
0
\right)
\right].
$$

Unlike a standard European option on a single asset, this expectation depends on the **joint distribution** of two correlated asset prices. Let's use quantum Monte Carlo to estimate it!

## Challenge Code

Complete the QNode `quantum_montecarlo` which estimates the value of the basket option using quantum Monte Carlo.

For this challenge, use the fixed market parameters

$$
S_{1,0}=S_{2,0}=100,
\qquad
\sigma_1=0.20,
\qquad
\sigma_2=0.30,
\qquad
r=0.05.
$$

Your are required to approximate the probability density function of  by discretizing each variable on the interval

$$
[-3,3],
$$

using 8 equally spaced points. Therefore, the are 64 $(z_1,z_2)$ points representing 64 possible market scenarios.

For each scenario, you will need evaluate the bivariate normal probability density

$$
p(z_1,z_2)
=
\frac{1}{2\pi\sqrt{1-\rho^2}}
\exp\left[
-\frac{
z_1^2-2\rho z_1z_2+z_2^2
}{
2(1-\rho^2)
}
\right],
$$

and normalize the resulting discrete probabilities so that

$$
\sum_i p_i=1.
$$

Next, calculate the terminal asset prices associated with each pair $(z_1,z_2)$, followed by the corresponding basket payoff.

Quantum Monte Carlo requires the function being averaged to take values between zero and one. You should therefore normalize the payoffs by their maximum value on the discretized grid,

$$
f(i)=\frac{g_i}{g_{\max}},
$$

where

$$
g_{\max}=\max_i g_i.
$$

You will need to implement all of the above as helper functions. You are given space to do so in the template.

After this, you may use PennyLane's built-in quantum Monte Carlo functionality to perform the quantum estimation.

Your quantum algorithm produces an estimate

$$
\mu\approx\mathbb E[f],
$$

This is the expectation of the **normalized** payoff. 

Important notes:

- Use 10 estimation wires. 
- **Please make the bottom (last) wires the estimation wires for the grader to work.**

This is all you will need to do. The grader will take your output and calculate the value of the basket option. This is done by extracting the estimated phase from the estimation wires, undoing the normalization and discounting the expected payoff back to the present:

$$
V_0
=
e^{-rT}g_{\max}\mu.
$$

### Inputs

As inputs to this problem, you are given:

* `K` (`float`): strike price of the basket option.
* `w` (`float`): weight of the first asset in the basket, with $0\leq w\leq1$.
* `rho` (`float`): correlation between the Brownian shocks of the two assets, with $-1<\rho<1$.
* `T` (`float`): time to maturity in years.

### Output

* (`float`): the quantum Monte Carlo estimate of the basket option's present value. This is calculated by the grader from the output of your Monte Carlo circuit.

Good luck!


### Test cases

The following **public test cases** are available to you. Note that there are additional **hidden test cases** that we use to verify that your code is valid in full generality.

The test inputs are arrays containing `K`, `w`, `rho` and `T` in that order.

```python
test_input: [0.3, 1.0, 1.0, 100]
expected_output: 10.556134590137553

test_input: [0.4, 0.5, 1.0, 110]
expected_output: = 6.487093067342844
```

If your solution matches the correct one within the given tolerance specified in `check` (in this case, it's a `1e-3` absolute error tolerance), the output will be `"Success!"` Otherwise, you will receive an `"Incorrect"` prompt.

Good luck!


