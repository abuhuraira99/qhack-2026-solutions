# Building a Quantum Kernel  (100 pts)

- **Group:** Group 2
- **Status:** PASSED (submitted 2026-10-19 18:05:14 UTC)
- **Hidden test cases:** yes

---

Kernel methods are a set of techniques that have gained a considerable amount of interest among the *classical* machine learning community. But what are they? How do they work? Well, kernel methods are built around the idea of kernels, which are functions that try to address how similar two data points are to one another by going into a high-dimensional feature space. It is believed that mapping the input data into a high-dimensional feature space will make it simpler to distinguish between classes or generate predictions.

One of the most well-known kernel methods is the support vector machine (SVM), a supervised binary classifier that aims to determine the hyperplane that most effectively divides data in two groups. 

<p align="center">
<img src="https://s3.us-east-1.amazonaws.com/swc-prod-event-content-qhack-2026/challenge-images/building_quantum_kernel/embedding_nonlinear_classification.png" width="400"/>
</p>

Cool! So far, so good, but where does the quantum part come into play? Let's start with some math!

The SVM algorithm will perform the binary classification of a data point according to the following expression:

$$
y(\vec{x})=sign\left(\langle\vec{w}, \vec{x}\rangle+b\right),
$$

where $\langle\vec{w}, \vec{x}\rangle$ denotes the inner product of the vector $\vec{w}$, which is perpendicular to the hyperplane, and the independent term $b$, which specifies the position on the hyperplane. Then, following the kernel's definition one can remap $\vec{x}$ into a larger feature space: $\vec{x} \rightarrow \phi(\vec{x})$. Also, one can rewrite $\vec{w}$ as a linear combination of the remapped datapoints: $\vec{w}=\sum_i \alpha_i \phi(\vec{x}_i)$. Putting this all together, the previous formula will read:

$$
y(\vec{x})=sign\left(\sum_i \alpha_i \langle\phi(\vec{x_i}), \phi(\vec{x})\rangle+b\right).
$$

Now the prediction only contains inner products in the enlarged feature space. These products are what we will call kernel functions:

$$
k(\vec{x}_i,\vec{x}_j)=\langle\phi(\vec{x_i}), \phi(\vec{x_j})\rangle.
$$

From this you can start guessing at the relation of this technique to quantum computing. This relation will naturally appear if we think of our feature space as a Hilbert space and our map $\phi(\vec{x})$ as a quantum state in such Hilbert space:

$$
|\phi(\vec{x})\rangle=S(\vec{x})|0\rangle,
$$

where $S(\vec{x})$ correspond to the embedding routine to prepare such a state.

Thus, we can now obtain our desired *quantum* kernel:

$$
k(\vec{x}_i,\vec{x}_j)=|\langle \phi(\vec{x_i})|\phi(\vec{x_j})\rangle|^2.
$$

Finally, this quantum kernel can be inserted as a subroutine to efficiently compute the kernel in a quantum approach in the SVM method to create the so-called quantum support vector machine (QSVM).

Then, after feeding our quantum machine learning model with data, one would be able to train the weights $\alpha_i$ to solve our target problem. This can easily be done using machine learning libraries such as `scikit-learn`, but that is of no interest of this challenge. Here we will focus on how to build a quantum kernel. Exciting, yeah? Let's get started!

## Challenge code

In the code below, you must complete two functions:

- `quantum_kernel`: A QNode that returns the value of the quantum kernel. **You must complete this function.** The arguments of this function are:
    
    - `x1` (`list(float)`): The first of the datapoints from which we want to compute the kernel.
    - `x2` (`list(float)`): The second of the datapoints from which we want to compute the kernel.

- `kernel_matrix`: A function that returns the matrix of pairwise kernel values for two given datapoints. **You must complete this function.** The arguments of this function are:

    - `X1` (`list(list(float))`): The first list of datapoints from which we want to compute the kernel matrix.
    - `X2` (`list(list(float))`): The second list of datapoints from which we want to compute the kernel matrix.


### Input 

As input to this problem, you are given:

- `X1` (`list(list(float))`): The first list of datapoints from which we want to compute the kernel matrix.
- `X1` (`list(list(float))`): The second list of datapoints from which we want to compute the kernel matrix.
### Output

This code must output an `np.array(float)` corresponding to the kernel matrix of the two input datasets. 

### Test cases

The test cases are given as lists of the form [`X1`, `X2`]. The following **public test cases** are available for you to check your work. There are also some **hidden test cases** which we will use to check that your solution works in full generality.

```python
test_input = [[[0.32058496, 0.07741205, 0.53200578, 0.91373749],[0.71838322, 0.45665254, 0.19871986, 0.1157332 ],[0.04515,    0.66228969, 0.69793587, 0.64664178]],
              [[0.32058496, 0.07741205, 0.53200578, 0.91373749],[0.71838322, 0.45665254, 0.19871986, 0.1157332 ],[0.04515,    0.66228969, 0.69793587, 0.64664178]]]
expected_output = [[1, 0.76528062, 0.87759179], 
                  [0.76528062, 1, 0.77075905], 
                  [0.87759179, 0.77075905, 1]]

test_input = [[[0.94727029, 0.40665627, 0.05521391, 0.06570142],[0.32897296, 0.89902984, 0.59060573, 0.11193315]],
              [[0.11815914, 0.47388796, 0.64337692, 0.59215516],[0.69635966, 0.65039949, 0.17727646, 0.76091743]]]
expected_output = [[0.71461545, 0.85406897],
                  [0.89085434, 0.81902278]]
```

If your solution matches the correct one within the given tolerance specified in check (in this case it's a 1e-4 relative error tolerance), the output will be`"Success!"`. Otherwise, you will receive an `"Incorrect"` prompt.

All the best!
