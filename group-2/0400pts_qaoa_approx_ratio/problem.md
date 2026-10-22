# Approximation Ratio for QAOA  (400 pts)

- **Group:** Group 2
- **Status:** PASSED (submitted 2026-10-19 18:26:07 UTC)
- **Hidden test cases:** yes

---

## Challenge Statement

The Quantum Approximate Optimization Algorithm (QAOA) is well-known due to its efficacy in solving combinatorial optimization problems. In this challenge, we will use it to solve the Minimum Vertex Cover problem. Then we will compare the QAOA output to the exact classical solution in order to determine how well the algorithm performs.

The Minimum Vertex Cover problems ask us to find a set of vertices in a graph such that all of the edges in the graph are connected to at least one vertex in the set. This set must also contain the smaller number of vertices. 

For example, in the figure below, the green vertices are in the set and the blue edges are adjacent to them. A vertex set that makes all edges in the graph blue is a vertex cover. Finding a minimum vertex cover amounts to finding the minimum amount of green vertices that makes all the edges blue.

<p align="center">
<img src="https://s3.us-east-1.amazonaws.com/swc-prod-event-content-qhack-2026/challenge-images/qaoa_approx_ratio/vertex_covers.png" width="400" alt>
</p>

Our objective in this challenge is to write a routine that solves this problem for an *arbitrary graph.* 

The cost Hamiltonian for this problem is given by

$$
H_{\text{cost}} = \frac{3}{4}\sum_{(i,j) \in \text{edges}}(Z_iZ_j +Z_i +Z_j) - \sum_{i \in \text{vertices}}Z_i
$$

and that the mixer Hamiltonian is

$$
H_{\text{mixer}} = \sum_{i \in \text{vertices}}X_i.
$$

You will to build these Hamiltonians, implement the QAOA circuit, and optimize the QAOA parameters to find the minimum expectation value of the cost Hamiltonian. Your ultimate task is to find the approximation ratio

$$
r^{*} = \frac{\text{Minimum expectation value estimated by QAOA}}{\text{True minimum eigenvalue of the cost Hamiltonian}}.
$$

The QAOA circuit consists of a series of a layer of Hadamard gates followed by the QAOA layers shown below.

<p align="center">
<img src="https://s3.us-east-1.amazonaws.com/swc-prod-event-content-qhack-2026/challenge-images/qaoa_approx_ratio/cost_mixer.png" width="400"/>
</p>

To grade your solution, we ask you to **use four of these QAOA layers.**

## Challenge code

You must complete the `approximation_ratio` function, which takes the `edges` of the graph as an argument. The `edges` list's elements are ordered pairs of integers representing each edge in the graph. The integers in each pair are the vertices joined by the edge. For example, the following graph

<p align="center">
<img src="https://s3.us-east-1.amazonaws.com/swc-prod-event-content-qhack-2026/challenge-images/qaoa_approx_ratio/vertex_graph.png" width="400"/>
</p>

is represented via `edges = [[0,1], [0,2], [1,2], [2,3]]`. 

The `approximation_ratio` function must return a `numpy.tensor` containing one real number.

You are also given some blank space to write any helper functions you may need.

### Input

As input to this problem, you are given the `edges` of the graph to solve for, as explained above.
 
### Output

This code will output a `float` corresponding to the approximation ratio of the depth-4 QAOA algorithm. This `float` will be automatically extracted from the output of your `approximation_ratio` function.

### Test cases

The following **public test cases** are available to you. Note that there are additional **hidden test cases** that we use to verify that your code is valid in full generality.

```python
test_input: [[0, 1], [1, 2], [0, 2], [2, 3]]
expected_output: 0.58160924

test_input: [[0, 1], [1, 2], [2, 3], [3, 0]]
expected_output: 0.94746734
```

If your solution matches the correct one within the given tolerance specified in `check` (in this case it's a `5e-2` relative error tolerance), the output will be `"Success!"` Otherwise, you will receive an `"Incorrect"` prompt.

Good luck!


