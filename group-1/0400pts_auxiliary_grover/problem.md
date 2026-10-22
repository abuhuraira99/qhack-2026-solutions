# Grover's Little Helper  (400 pts)

- **Group:** Group 1
- **Status:** PASSED (submitted 2026-10-19 16:47:51 UTC)
- **Hidden test cases:** yes

---

Grover's Algorithm is an oracle-based quantum algorithm for unstructured search in lists of $N$ items that finds—with high probability—the correct solutions using $\mathcal{O}(\sqrt{N})$ queries of the list, whereas any classical algorithm would require $\mathcal{O}(N)$ queries. This proven quadratic speedup makes Grover's algorithm one of the most promising quantum algorithms out there!

The workflow of Grover's algorithm consists of the following:

1. Prepare a uniform superposition of $n = \log_2(N)$ qubits: $|\psi\rangle=\frac{1}{\sqrt{N}}\sum_{x=0}^{N-1}|x\rangle$.
2. Apply the oracle operator, which marks the sought-after states $|\omega \rangle$ with a minus sign.
3. Apply the diffusion operator to increase the amplitude of the states marked by the oracle.
4. Repeat 2 and 3 and measure.

The quantum circuit that represents Grover's algorithm for 2 qubits, with no additional ancillary qubits, is:

<p align="center">
<img src="https://s3.us-east-1.amazonaws.com/swc-prod-event-content-qhack-2026/challenge-images/auxiliary_grover/grover_2qubits.png" width="400"/>
</p>


---
**NOTE**: Each computational basis state corresponds to one of the items in the list we are searching.


---

However, even masterpieces such as this algorithm have their own limitations! In this challenge, we will focus on one of the drawbacks of this algorithm with the goal to overcome it. In particular, for Grover's algorithm, it is especially challenging to find a solution when the number of solutions is half the total number of items, i.e. $N/2$. In this case,  each iteration of Grover's operator (a combination of the oracle and diffusion operator), does not increase the amplitude of the solution states. You can check that yourself for one or two qubit circuits.

Can we still hope to find the solutions using Grover search? Of course we can!

To overcome this limitation we only need one auxiliary qubit! In fact, with one auxiliary qubit, we can design a circuit that requires applying the oracle and diffusion operator only once. Moreover, with one single shot, such circuit is able to provide one of the possible solutions!

In this challenge you are asked to design such a circuit! To avoid overcomplicating things, we will focus on the 2-qubit case, with four possible basis states:

$$
|00\rangle, |01\rangle, |10\rangle, |11\rangle.
$$

Two of them (you don't know which ones, but the oracle does 😉) are solutions. So, using ONLY one auxiliary qubit and ONLY one shot, you should be able to measure a quantum state that corresponds to one of the solutions.


## Challenge code

In the code below, you must complete this function:

- `circuit`: a QNode that returns a dictionary with the counts on the two first wires. The arguments of this function are:
    
    - `generator` (`function`): A function that initializes the quantum state to the uniform state
    - `oracle` (`function`): A function that marks the desired states        
    - `diffuser` (`function`): A function that amplifies the states marked by the oracle         

### Input 

In this challenge there is no input. However, you can use the `generator`, `oracle` and `diffuser` functions, which can be called in the following way: `generator()`, `oracle()` and `diffuser(generator)`. Note that they all act over the first two qubits.

### Output

To judge this challenge, we will generate 1000 different oracles. Then, we will run your `circuit` function for each oracle to check that your predictions are correct. Therefore, in this case, there will be no public and private test cases. 

All the best!
